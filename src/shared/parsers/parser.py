# src/infrastructure/parser/parser.py
import asyncio
import os
import logging

import aiohttp

from src.core.domain.entities.branch import Branch
from src.core.domain.entities.category import Category
from src.core.domain.entities.product import Product

from src.infrastructure.database.dao.branch_dao import BranchDAO
from src.infrastructure.database.dao.category_dao import CategoryDAO
from src.infrastructure.database.dao.product_dao import ProductDAO

from src.infrastructure.database.repositories.branch_repo_impl import BranchRepositoryImpl
from src.infrastructure.database.repositories.category_repo_impl import CategoryRepositoryImpl
from src.infrastructure.database.repositories.product_repo_impl import ProductRepositoryImpl

from src.infrastructure.database.models.base import async_session_maker

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

API_URL  = "https://us-central1-marmar-eab6d.cloudfunctions.net/getDishes"
API_PASS = "qpwiugh08q34gowipewcg087wte7tweiubhwiug08ywgg837g48g20873g3"

BRANCHES = {
    "dishes":  "Филиал 1",
    "dishes2": "Филиал 2",
    "dishes3": "Филиал 3",
}


class Parser:

    def __init__(self, session):
        self.branch_repo   = BranchRepositoryImpl(BranchDAO(session))
        self.category_repo = CategoryRepositoryImpl(CategoryDAO(session))
        self.product_repo  = ProductRepositoryImpl(ProductDAO(session))

    @staticmethod
    async def _fetch_dishes(http: aiohttp.ClientSession, branch_code: str) -> dict:
        url = f"{API_URL}?filial={branch_code}&password={API_PASS}"
        try:
            async with http.get(url) as resp:
                if resp.status == 200:
                    return await resp.json(content_type=None)
                logging.error(f"API статус {resp.status} для {branch_code}")
                return {}
        except Exception as e:
            logging.error(f"Сетевая ошибка для {branch_code}: {e}")
            return {}

    async def _get_or_create_branch(self, branch_code: str, name: str) -> Branch:
        existing = await self.branch_repo.get_list(limit=1, branch_code=branch_code)
        if existing:
            return existing[0]

        branch = await self.branch_repo.add(Branch(
            id=None,
            name=name,
            branch_code=branch_code,
            description="",
            address="",
            landmark="",
            latitude=None,
            longitude=None,
            delivery_price=0,
            is_active=True,
        ))
        logging.info(f"Создан филиал: {name} (ID: {branch.id})")
        return branch

    async def _get_or_create_category(self, name: str, branch_id: int, cache: dict) -> int:
        key = (name, branch_id)
        if key in cache:
            return cache[key]

        existing = await self.category_repo.get_list(limit=1, name=name, branch_id=branch_id)
        if existing:
            cache[key] = existing[0].id
            return existing[0].id

        cat = await self.category_repo.add(Category(
            id=None,
            name=name,
            description="",
            branch_id=branch_id,
            is_active=True,
        ))
        cache[key] = cat.id
        logging.info(f"  Создана категория: {name} (ID: {cat.id})")
        return cat.id

    async def _save_or_update_product(
        self, api_id: str, item: dict, category_id: int, branch_id: int, img_url: str
    ) -> Product:
        name = item.get("name") or item.get("runame") or "Без названия"

        existing = await self.product_repo.get_list(limit=1, api_id=api_id)
        if existing:
            p = existing[0]
            p.name              = name
            p.uzname            = item.get("uzname", "")
            p.runame            = item.get("runame", "")
            p.enname            = item.get("enname", "")
            p.description       = item.get("desc", "")
            p.price             = float(item.get("price", 0))
            p.category_id       = category_id
            p.subcategory_index = int(item.get("subcategoryindex", 0))
            p.img               = img_url
            p.image_url         = img_url
            return await self.product_repo.update(p)

        return await self.product_repo.add(Product(
            id=None,
            api_id            = api_id,
            name              = name,
            uzname            = item.get("uzname", ""),
            runame            = item.get("runame", ""),
            enname            = item.get("enname", ""),
            description       = item.get("desc", ""),
            price             = float(item.get("price", 0)),
            category_id       = category_id,
            subcategory_index = int(item.get("subcategoryindex", 0)),
            branch_id         = branch_id,
            img               = img_url,
            image_url         = img_url,
            img_file_id       = None,
            is_active         = True,
            maintenance_day   = None,
            maintenance_night = None,
        ))

    async def sync_all(self):
        logging.info("=== Начало синхронизации меню ===")

        async with aiohttp.ClientSession() as http:
            for branch_code, branch_name in BRANCHES.items():
                logging.info(f"--- Филиал: {branch_name} ({branch_code}) ---")

                branch   = await self._get_or_create_branch(branch_code, branch_name)
                raw_data = await self._fetch_dishes(http, branch_code)

                if not raw_data:
                    logging.warning(f"Нет данных для {branch_code}, пропускаем.")
                    continue

                category_cache: dict = {}
                ok = 0

                for api_id, item in raw_data.items():
                    try:
                        cat_name    = item.get("category") or "Без категории"
                        category_id = await self._get_or_create_category(
                            cat_name, branch.id, category_cache
                        )
                        img_url = item.get("img") or ""
                        await self._save_or_update_product(
                            api_id      = str(api_id),
                            item        = item,
                            category_id = category_id,
                            branch_id   = branch.id,
                            img_url     = img_url,
                        )
                        ok += 1
                    except Exception as e:
                        logging.error(f"Ошибка товара {api_id}: {e}")

                logging.info(f"Готово: {ok} товаров для филиала {branch_name}.")

        logging.info("=== Синхронизация завершена ✅ ===")


async def main():
    async with async_session_maker() as session:
        parser = Parser(session)
        await parser.sync_all()


if __name__ == "__main__":
    asyncio.run(main())