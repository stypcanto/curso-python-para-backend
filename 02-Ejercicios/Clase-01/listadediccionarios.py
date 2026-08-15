request = [
    {
        "id": 1001,
        "title": "Clase 01 - Ejercicios",
        "estimated_hours": 2.5,
        "is_active": True,
        "assigned_user": "styp"
    },
    {
        "id": 1002,
        "title": "Clase 02 - Ejercicios",
        "estimated_hours": 3.0,
        "is_active": False,
        "assigned_user": "jdoe"
    }
]

for req in request:
    print(f"Request ID: {req['id']}")
    print(f"Request Title: {req['title']}")
    print(f"Estimated Hours: {req['estimated_hours']}")
    print(f"Is Active: {req['is_active']}")
    print(f"Assigned User: {req['assigned_user']}")
    print()  # Print a blank line for better readability

#print(f"Request ID: {request[0]['id']}")
#print(f"Request Title: {request[0]['title']}")