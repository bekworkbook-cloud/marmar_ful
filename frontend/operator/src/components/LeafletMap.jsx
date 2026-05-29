// src/components/LeafletMap.jsx
import { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Импортируем сам Leaflet для исправления дефолтных путей к иконкам маркеров в Vite
import L from 'leaflet';

// Фикс бага Vite + Leaflet с ломающимися путями к иконкам маркеров
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Вспомогательный внутренний компонент для динамического обновления центра карты при смене заказа
function ChangeMapView({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center && center[0] !== 0) {
      map.setView(center, map.getZoom());
    }
  }, [center, map]);
  return null;
}

export default function LeafletMap({ latitude, longitude }) {
  // Безопасный фолбек на случай непредвиденных пустых координат
  const position = [latitude || 0, longitude || 0];

  if (latitude === 0 || !latitude || longitude === 0 || !longitude) {
    return (
      <div className="w-full h-full bg-slate-900 flex items-center justify-center text-xs text-slate-500 font-medium">
        Координаты точки недоступны
      </div>
    );
  }

  return (
    <MapContainer 
      center={position} 
      zoom={15} 
      zoomControl={false} // Отключаем дефолтные кнопки +/- для компактности в Mini App
      className="w-full h-full"
      style={{ background: '#020617' }} // Соответствует slate-950 бэкграунда панели
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      {/* Рендерим маркер на точке доставки (перетаскивание dragging={false} отключено) */}
      <Marker position={position} dragging={false} />
      
      {/* Слушатель для изменения фокуса карты при переключении между заказами */}
      <ChangeMapView center={position} />
    </MapContainer>
  );
}