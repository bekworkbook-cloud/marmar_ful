// src/components/LeafletMap.jsx
import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Фикс дефолтных иконок Leaflet в Vite сборках
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

// Вспомогательный компонент для обновления центра карты при изменении координат
function ChangeMapView({ center }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, map.getZoom());
  }, [center, map]);
  return null;
}

export default function LeafletMap({ latitude, longitude }) {
  // Защита от нулевых или дефолтных координат
  if (!latitude || !longitude || latitude === 0 || longitude === 0) {
    return (
      <div className="w-full h-48 bg-slate-100 dark:bg-slate-800 rounded-xl flex items-center justify-center border border-dashed border-slate-300 text-sm text-slate-400">
        Координаты доставки не указаны
      </div>
    );
  }

  const position = [latitude, longitude];

  return (
    <div className="w-full h-56 rounded-xl overflow-hidden shadow-inner border border-slate-200 dark:border-slate-700 z-10 relative">
      <MapContainer 
        center={position} 
        zoom={15} 
        dragging={false}
        touchZoom={false}
        scrollWheelZoom={false}
        doubleClickZoom={false}
        zoomControl={false}
        className="w-full h-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position} />
        <ChangeMapView center={position} />
      </MapContainer>
    </div>
  );
}