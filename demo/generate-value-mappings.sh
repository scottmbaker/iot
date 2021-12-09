set -e

AETHER_PROD_SRC='Aether Connected Edge-1638471725021.json'
AETHER_MENLO_SRC='menlo-dashboard.txt'

curl --fail --location --request GET 'https://roc.aetherproject.org/aether-roc-api/aether/v3.0.0/connectivity-service-v3/device-group' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $AETHER_PROD_AUTH" > all_dg.json
python ./keys_to_valuemaps.py < all_dg.json > value_mappings.json
python ./update_dashboard.py < "$AETHER_PROD_SRC" > aether-prod-updated.json

curl --fail --location --request GET 'https://roc.menlo.aetherproject.org/aether-roc-api/aether/v4.0.0/connectivity-service-v4/device-group' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $AETHER_MENLO_AUTH" > all_dg.json
python ./keys_to_valuemaps.py < all_dg.json > value_mappings.json
python ./update_dashboard.py < "$AETHER_MENLO_SRC" > aether-menlo-updated.json

rm -f all_dg.json value_mappings.json
