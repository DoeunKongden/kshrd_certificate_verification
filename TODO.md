# TODO: Upgrade verify_certificate logic to include Template Layout:
# 1. Fetch Certificate by code (Existing logic).
# 2. Use joinedload to get CertificateType -> Template in a single query.
# 3. Cache the MERGED result in Redis (95% speed boost maintained).
# 4. Response structure should be:
#    {
#      "data": { "student_name": "...", "id": "...", ... },
#      "layout": [ { "type": "text", "x": 100, "y": 200, "label": "student_name" }, ... ]
#    }
# 5. Note: The frontend will use the 'label' in the layout to find 
#    the matching value in the 'data' object.