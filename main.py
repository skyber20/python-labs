from task_processor.sources.api_source import ApiSource
from task_processor.sources.file_source import JsonFileSource
from task_processor.sources.generator_source import GeneratorSource
from task_processor.aggregator import Aggregator


def main():
    good_file_source = JsonFileSource("data/good_file.json")
    good_with_bad_file_source = JsonFileSource("data/good_with_bad_tasks.json")
    not_exists_file_source = JsonFileSource("data/not_exists_file.json")
    generator_source = GeneratorSource(5)
    api_source = ApiSource()

    sources = [
        good_file_source,
        good_with_bad_file_source,
        not_exists_file_source,
        generator_source,
        api_source
    ]

    aggregator = Aggregator(sources)

    for task in aggregator.get_tasks():
        print(task.id)
        print(task.payload)
        print()


if __name__ == '__main__':
    main()
