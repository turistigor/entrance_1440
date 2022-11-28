from datetime import datetime


def get_current_data(shared_data):
    channels = []
    for ch in shared_data:
        update_dt = datetime.fromtimestamp(ch.update_dt)
        channels.append({
            'num': ch.num,
            'current': ch.current,
            'voltage': ch.voltage,
            'update_dt': update_dt.isoformat()
        })
    return {
        'channels': channels
    }