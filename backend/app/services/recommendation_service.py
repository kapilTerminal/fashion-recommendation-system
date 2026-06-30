def recommendation_service(data):
    return {
        "message": "AI recommendation service is working",
        "received_data": data.model_dump()
    }