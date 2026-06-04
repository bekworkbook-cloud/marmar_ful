// components/LeafletMap.jsx

import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function MapClickHandler({ onMapClick }) {
  useMapEvents({
    click(e) {
      onMapClick(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

export default function LeafletMap({ latitude, longitude, onMapClick }) {
  return (
    <MapContainer
      center={[41.311081, 69.240562]}
      zoom={12}
      // ✅ FIX: tap must be true for mobile/Telegram WebView touch events
      tap={true}
      style={{ width: '100%', height: '100%', touchAction: 'none' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapClickHandler onMapClick={onMapClick} />
      {latitude !== 0 && longitude !== 0 && (
        <Marker position={[latitude, longitude]} />
      )}
    </MapContainer>
  );
}
