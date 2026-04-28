"use client";

import { importLibrary, setOptions } from "@googlemaps/js-api-loader";
import { useEffect, useRef, useState } from "react";
import type { Pin } from "@/types/locationiq";

type ExactPinMapProps = {
  pin?: Pin;
};

export function ExactPinMap({ pin }: ExactPinMapProps) {
  const mapElementRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<google.maps.Map | null>(null);
  const markerRef = useRef<google.maps.marker.AdvancedMarkerElement | google.maps.Marker | null>(
    null,
  );
  const [mapType, setMapType] = useState<"roadmap" | "satellite">("roadmap");
  const [loadError, setLoadError] = useState<string | null>(null);
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

  useEffect(() => {
    if (!pin || !apiKey || !mapElementRef.current) return;

    let cancelled = false;
    const position = { lat: pin.latitude, lng: pin.longitude };

    async function initialiseMap() {
      try {
        setOptions({ key: apiKey, v: "weekly" });
        const { Map } = (await importLibrary("maps")) as google.maps.MapsLibrary;
        const map =
          mapRef.current ??
          new Map(mapElementRef.current as HTMLElement, {
            center: position,
            zoom: 17,
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: false,
            mapTypeId: mapType,
          });

        if (cancelled) return;

        mapRef.current = map;
        map.setCenter(position);
        map.setZoom(17);
        map.setMapTypeId(mapType);

        if (!markerRef.current) {
          try {
            const { AdvancedMarkerElement } = (await importLibrary(
              "marker",
            )) as google.maps.MarkerLibrary;
            markerRef.current = new AdvancedMarkerElement({
              map,
              position,
              title: "Exact LocationIQ pin",
            });
          } catch {
            markerRef.current = new google.maps.Marker({
              map,
              position,
              title: "Exact LocationIQ pin",
            });
          }
        } else {
          if ("setPosition" in markerRef.current) {
            markerRef.current.setMap(map);
            markerRef.current.setPosition(position);
          } else {
            markerRef.current.map = map;
            markerRef.current.position = position;
          }
        }
      } catch {
        setLoadError("Google Maps could not load. The exact coordinate is still preserved.");
      }
    }

    initialiseMap();
    return () => {
      cancelled = true;
    };
  }, [apiKey, mapType, pin]);

  if (!pin) {
    return (
      <div className="map-canvas">
        <div className="map-grid" />
        <div className="map-empty">Waiting for a coordinate</div>
      </div>
    );
  }

  if (!apiKey || loadError) {
    return (
      <div className="map-canvas">
        <div className="map-grid" />
        <div className="pin-marker" />
        <CoordinateStrip pin={pin} />
        {loadError ? <div className="map-warning">{loadError}</div> : null}
      </div>
    );
  }

  return (
    <div className="map-canvas">
      <div ref={mapElementRef} className="google-map" />
      <div className="map-toggle" aria-label="Map type">
        <button
          className={mapType === "roadmap" ? "selected" : ""}
          onClick={() => setMapType("roadmap")}
          type="button"
        >
          Map
        </button>
        <button
          className={mapType === "satellite" ? "selected" : ""}
          onClick={() => setMapType("satellite")}
          type="button"
        >
          Satellite
        </button>
      </div>
      <CoordinateStrip pin={pin} />
    </div>
  );
}

function CoordinateStrip({ pin }: { pin: Pin }) {
  return (
    <div className="coordinate-strip">
      <span>Exact pin</span>
      <strong>
        {pin.latitude.toFixed(6)}, {pin.longitude.toFixed(6)}
      </strong>
    </div>
  );
}
