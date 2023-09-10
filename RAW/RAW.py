import datasets


_CITATION = """\
@inproceedings{luong-vu-2016-non,
    title = "A non-expert {K}aldi recipe for {V}ietnamese Speech Recognition System",
    author = "Luong, Hieu-Thi  and
      Vu, Hai-Quan",
    booktitle = "Proceedings of the Third International Workshop on Worldwide Language Service Infrastructure and Second Workshop on Open Infrastructures and Analysis Frameworks for Human Language Technologies ({WLSI}/{OIAF}4{HLT}2016)",
    month = dec,
    year = "2016",
    address = "Osaka, Japan",
    publisher = "The COLING 2016 Organizing Committee",
    url = "https://aclanthology.org/W16-5207",
    pages = "51--55",
}
"""

_DESCRIPTION = """\
VIVOS is a free Vietnamese speech corpus consisting of 15 hours of recording speech prepared for
Vietnamese Automatic Speech Recognition task.
The corpus was prepared by AILAB, a computer science lab of VNUHCM - University of Science, with Prof. Vu Hai Quan is the head of.
We publish this corpus in hope to attract more scientists to solve Vietnamese speech recognition problems.
"""

_HOMEPAGE = "https://doi.org/10.5281/zenodo.7068130"

_LICENSE = "CC BY-NC-SA 4.0"

# Source data: "https://zenodo.org/record/7068130/files/vivos.tar.gz"
_DATA_URL = "data/RAW.tar.gz"

_PROMPTS_URLS = {
    "train": "data/prompts-train.txt.gz",
    "dev": "data/prompts-dev.txt.gz",
    "test": "data/prompts-test.txt.gz",
}

_INWAVES = {
    "6": "RAWTRAIN",
    "_": "RAWTEST",
}


class RAWDataset(datasets.GeneratorBasedBuilder):
    """VIVOS is a free Vietnamese speech corpus consisting of 15 hours of recording speech prepared for
    Vietnamese Automatic Speech Recognition task."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    # "speaker_id": datasets.Value("string")
                    "path": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    "sentence": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        prompts_paths = dl_manager.download_and_extract(_PROMPTS_URLS)
        archive = dl_manager.download(_DATA_URL)
        train_dir = "RAW/train"
        dev_dir = "RAW/dev"
        test_dir = "RAW/test"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "prompts_path": prompts_paths["train"],
                    "path_to_clips": train_dir + "/waves",
                    "audio_files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "prompts_path": prompts_paths["dev"],
                    "path_to_clips": dev_dir + "/waves",
                    "audio_files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "prompts_path": prompts_paths["test"],
                    "path_to_clips": test_dir + "/waves",
                    "audio_files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, prompts_path, path_to_clips, audio_files):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.
        examples = {}
        with open(prompts_path, encoding="utf-8") as f:
            for row in f:
                data = row.strip().split("\t", 1)
                filename = data[0]
                parentfolder = _INWAVES[filename[0]]
                # speaker_id = data[0].split("_")[0]
                audio_path = "/".join([path_to_clips, parentfolder, filename + ".wav"])
                examples[audio_path] = {
                    "path": audio_path,
                    "sentence": data[1],
                }
        inside_clips_dir = False
        id_ = 0
        for path, f in audio_files:
            if path.startswith(path_to_clips):
                inside_clips_dir = True
                if path in examples:
                    audio = {"path": path, "bytes": f.read()}
                    yield id_, {**examples[path], "audio": audio}
                    id_ += 1
            elif inside_clips_dir:
                break
