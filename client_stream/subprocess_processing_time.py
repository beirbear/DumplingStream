from .configuration import Setting


class ProcessingTimeCollector:
    __records = {}
    __cyclic_max_length = Setting.get_max_processing_time_record()

    @staticmethod
    def add_info(creation_time, processing_time):
        ProcessingTimeCollector.__records[creation_time] = processing_time
        print("record:", str(ProcessingTimeCollector.__records))

    @staticmethod
    def get_avg_processing_time():
        total_time = 0.0
        for processing_time in ProcessingTimeCollector.__records.values():
            total_time += processing_time

        if not len(ProcessingTimeCollector.__records):
            return 0.0

        return total_time / len(ProcessingTimeCollector.__records)

    @staticmethod
    def get_sum_report():
        total_time = 0.0
        for processing_time in ProcessingTimeCollector.__records.values():
            total_time += processing_time

        return {"total_request": len(ProcessingTimeCollector.__records),
                "total_time": total_time}
