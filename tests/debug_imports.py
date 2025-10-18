try:
    print("Importando BlacklistResource...")
    from resources.blacklist_resource import BlacklistResource
    print("OK BlacklistResource importado correctamente")
    
    print("Importando GetBlacklistResource...")
    from resources.get_blacklist_resource import GetBlacklistResource
    print("OK GetBlacklistResource importado correctamente")
    
    print("Importando extensiones...")
    from extensions import api
    print("OK API importada correctamente")
    
    print("Registrando recursos...")
    api.add_resource(BlacklistResource, '/blacklist')
    api.add_resource(GetBlacklistResource, '/blacklist/<string:email>')
    print("OK Recursos registrados correctamente")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()