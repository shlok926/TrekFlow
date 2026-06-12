# src/ui/map_renderer.py
import json

def generate_google_map_html(starting_point, destination, spots):
    """
    Generates an HTML string containing a Leaflet map styled with Google Maps road tiles.
    - starting_point: dict with {"name": str, "latitude": float, "longitude": float} or None
    - destination: dict with {"name": str, "latitude": float, "longitude": float}
    - spots: list of dicts, each with {"name": str, "latitude": float, "longitude": float}
    """
    
    # Serialize parameters for JS injection
    starting_point_js = json.dumps(starting_point)
    destination_js = json.dumps(destination)
    spots_js = json.dumps(spots)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Google Map Route</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
        <style>
            html, body, #map {{
                height: 100%;
                width: 100%;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }}
            .leaflet-popup-content-wrapper {{
                border-radius: 8px;
                box-shadow: 0 3px 14px rgba(0,0,0,0.2);
            }}
            .popup-title {{
                font-weight: bold;
                font-size: 14px;
                color: #333;
                margin-bottom: 4px;
            }}
            .popup-desc {{
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
        <script>
            // Parse injected python data
            var startingPoint = {starting_point_js};
            var destination = {destination_js};
            var spots = {spots_js};

            // Set default view (centered at destination)
            var map = L.map('map').setView([destination.latitude, destination.longitude], 13);

            // Add official Google Maps road tiles via subdomains
            var googleStreets = L.tileLayer('https://{{s}}.google.com/vt/lyrs=m&x={{x}}&y={{y}}&z={{z}}', {{
                maxZoom: 20,
                subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
                attribution: '&copy; <a href="https://maps.google.com/">Google Maps</a>'
            }}).addTo(map);

            var markers = [];
            var bounds = [];

            // 1. Add Starting Point if specified
            if (startingPoint && startingPoint.latitude && startingPoint.longitude) {{
                var startLatLng = [startingPoint.latitude, startingPoint.longitude];
                bounds.push(startLatLng);

                var startIcon = L.divIcon({{
                    className: 'custom-div-icon',
                    html: "<div style='background-color:#E65100; color:white; border:2px solid white; border-radius:50%; width:32px; height:32px; display:flex; justify-content:center; align-items:center; font-size:16px; font-weight:bold; box-shadow:0 0 10px rgba(230,81,0,0.6);'>🏠</div>",
                    iconSize: [32, 32],
                    iconAnchor: [16, 16]
                }});

                var startMarker = L.marker(startLatLng, {{ icon: startIcon }}).addTo(map);
                startMarker.bindPopup("<div class='popup-title'>🏠 Starting Point</div><div class='popup-desc'>" + startingPoint.name + "</div>");
                markers.push(startMarker);

                // Add travel path connection line from starting point to destination
                var destLatLng = [destination.latitude, destination.longitude];
                var travelLine = L.polyline([startLatLng, destLatLng], {{
                    color: '#E65100',
                    weight: 3,
                    opacity: 0.6,
                    dashArray: '5, 8'
                }}).addTo(map);
                travelLine.bindTooltip("Travel Route from " + startingPoint.name + " to " + destination.name, {{
                    permanent: false,
                    direction: 'center'
                }});
            }}

            // 2. Add Destination Center
            var destLatLng = [destination.latitude, destination.longitude];
            bounds.push(destLatLng);

            var destIcon = L.divIcon({{
                className: 'custom-div-icon',
                html: "<div style='background-color:#0D47A1; color:white; border:2px solid white; border-radius:50%; width:32px; height:32px; display:flex; justify-content:center; align-items:center; font-size:16px; font-weight:bold; box-shadow:0 0 10px rgba(13,71,161,0.6);'>📍</div>",
                iconSize: [32, 32],
                iconAnchor: [16, 16]
            }});

            var destMarker = L.marker(destLatLng, {{ icon: destIcon }}).addTo(map);
            destMarker.bindPopup("<div class='popup-title'>📍 " + destination.name + " Hub</div><div class='popup-desc'>Center of your trip!</div>");
            markers.push(destMarker);

            // 3. Add Sightseeing Spots and sequential lines
            var routeLatLngs = [];
            
            // Connect starting at the center, or just connect spots
            // Let's connect spots sequentially
            spots.forEach(function(spot, index) {{
                var spotLatLng = [spot.latitude, spot.longitude];
                bounds.push(spotLatLng);
                routeLatLngs.push(spotLatLng);

                var spotIcon = L.divIcon({{
                    className: 'custom-div-icon',
                    html: "<div style='background: linear-gradient(135deg, #8A2BE2, #4A0E4E); color:white; border:2px solid white; border-radius:50%; width:26px; height:26px; display:flex; justify-content:center; align-items:center; font-size:11px; font-weight:bold; box-shadow:0 0 8px rgba(138,43,226,0.6);'>" + (index + 1) + "</div>",
                    iconSize: [26, 26],
                    iconAnchor: [13, 13]
                }});

                var spotMarker = L.marker(spotLatLng, {{ icon: spotIcon }}).addTo(map);
                spotMarker.bindPopup("<div class='popup-title'>📌 Spot " + (index + 1) + ": " + spot.name + "</div><div class='popup-desc'>Part of your custom itinerary.</div>");
                markers.push(spotMarker);
            }});

            // Draw solid line connecting destination spots in sequence
            if (routeLatLngs.length > 1) {{
                var itineraryLine = L.polyline(routeLatLngs, {{
                    color: '#8A2BE2',
                    weight: 4,
                    opacity: 0.8
                }}).addTo(map);
                itineraryLine.bindTooltip("Sightseeing Route Path", {{
                    permanent: false,
                    direction: 'center'
                }});
            }}

            // Fit map to contain all elements nicely
            if (bounds.length > 0) {{
                var group = new L.featureGroup(markers);
                map.fitBounds(group.getBounds().pad(0.15));
            }}
        </script>
    </body>
    </html>
    """
    return html_content
