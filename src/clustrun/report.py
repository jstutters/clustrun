from datetime import datetime, timedelta
from queue import Empty


def make_report(config, start_time, results):
    results = _queue_to_list(results)
    return {
        'config': config.to_dict(),
        'results': [r.to_dict() for r in results],
        'summary': {
            'start_time': str(start_time),
            'total_duration': str(_calculate_mean_duration(results)),
            'mean_duration': str(_calculate_mean_duration(results)),
            'finish_time': str(datetime.now()),
            'num_tasks': len(results),
            'num_successes': _calculate_num_successes(results),
            'num_failures': _calculate_num_failures(results),
        }
    }


def _queue_to_list(queued_items):
    items = []
    while True:
        try:
            items.append(queued_items.get(block=False))
        except Empty:
            break
    return items


def _calculate_total_duration(results):
    return timedelta(seconds=sum([r.duration.total_seconds() for r in results]))


def _calculate_mean_duration(results):
    return timedelta(seconds=_calculate_total_duration(results).total_seconds() / len(results))


def _calculate_num_successes(results):
    return len([r for r in results if r.exit_code == 0])


def _calculate_num_failures(results):
    return len([r for r in results if r.exit_code != 0])
