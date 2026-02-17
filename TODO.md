# TODO: Implement Certificate Template CRUD with the following requirements:
# 1. POST /templates/
#    - Schema: Use TemplateCreate (vaildates layout_config as List[TemplateElement]).
#    - Logic: 
#        - Check if template name already exists to prevent duplicates.
#        - Map layout_config elements using [e.model_dump() for e in payload.layout_config].
#        - Commit to PostgreSQL (JSONB column).
#    - Response: TemplateRead (201 Created).
#
# 2. GET /templates/
#    - Logic: Fetch all templates using sqlalchemy.future.select.
#    - Response: List[TemplateRead].
#
# 3. GET /templates/{id}
#    - Logic: Fetch single template by UUID. Raise 404 if not found.
#
# 4. Best Practice: Ensure AsyncSession is used via Depends(get_db).