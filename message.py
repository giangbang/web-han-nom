def success(data):
  return {"success":True, "data":data}
  
def error(e):
  return {"success":False, "data":e}