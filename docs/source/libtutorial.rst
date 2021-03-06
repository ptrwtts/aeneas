.. _libtutorial:

aeneas Library Tutorial
=======================

Overview
~~~~~~~~

Although a majority of ``aeneas`` users work with the built-in command line tools,
``aeneas`` is primarily designed for being used as a Python library.
Even the ``aeneas.tools`` can be used programmatically,
thanks to their standardize I/O interface.

.. Topic:: Example

    Create a Task and process it, outputting the resulting sync map to file::

        #!/usr/bin/env python
        # coding=utf-8

        from aeneas.executetask import ExecuteTask
        from aeneas.task import Task

        # create Task object
        config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
        task = Task(config_string=config_string)
        task.audio_file_path_absolute = u"/path/to/input/audio.mp3"
        task.text_file_path_absolute = u"/path/to/input/plain.txt"
        task.sync_map_file_path_absolute = u"/path/to/output/syncmap.json"

        # process Task
        ExecuteTask(task).execute()

        # output sync map to file
        task.output_sync_map_file()

    You can also use :class:`~aeneas.tools.execute_task.ExecuteTaskCLI`::

        #!/usr/bin/env python
        # coding=utf-8

        from aeneas.tools.execute_task import ExecuteTaskCLI

        ExecuteTaskCLI(use_sys=False).run(arguments=[
            None, # dummy program name argument
            u"/path/to/input/audio.mp3",
            u"/path/to/input/plain.txt",
            u"task_language=eng|is_text_type=plain|os_task_file_format=json",
            u"/path/to/output/syncmap.json"
        ])

Clearly, you can also manipulate objects programmatically.

.. Topic:: Example

    Create a Task, process it, and print all fragments in the resulting sync map
    whose duration is less than five seconds::

        #!/usr/bin/env python
        # coding=utf-8

        from aeneas.executetask import ExecuteTask
        from aeneas.task import Task

        # create Task object
        config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
        task = Task(config_string=config_string)
        task.audio_file_path_absolute = u"/path/to/input/audio.mp3"
        task.text_file_path_absolute = u"/path/to/input/plain.txt"

        # process Task
        ExecuteTask(task).execute()

        # print short fragments
        for fragment in task.sync_map.fragments_tree.vleaves_not_empty:
            if fragment.end - fragment.begin < 5.0:
                print(fragment)

Instead of passing around configuration strings,
you can set properties explicitly,
using the library functions and constants.

.. Topic:: Example

    Create a Task, process it, and print the resulting sync map::
    
        #!/usr/bin/env python
        # coding=utf-8

        from aeneas.executetask import ExecuteTask
        from aeneas.language import Language
        from aeneas.syncmap import SyncMapFormat
        from aeneas.task import Task
        from aeneas.task import TaskConfiguration
        from aeneas.textfile import TextFileFormat
        from aeneas.timevalue import TimeValue
        import aeneas.globalconstants as gc

        # create Task object
        config = TaskConfiguration()
        config[gc.PPN_TASK_LANGUAGE] = Language.ENG
        config[gc.PPN_TASK_IS_TEXT_FILE_FORMAT] = TextFileFormat.PLAIN
        config[gc.PPN_TASK_OS_FILE_FORMAT] = SyncMapFormat.JSON
        task = Task()
        task.configuration = config
        task.audio_file_path_absolute = u"/path/to/input/audio.mp3"
        task.text_file_path_absolute = u"/path/to/input/plain.txt"

        # process Task
        ExecuteTask(task).execute()

        # print produced sync map
        print(task.sync_map)



Dependencies
------------

* ``numpy`` (v1.9 or later)
* ``lxml`` (v3.0 or later)
* ``BeautifulSoup`` (v4.4 or later)

Only ``numpy`` is actually needed, as it is heavily used for the alignment computation.

The other two dependencies (``lxml`` and ``BeautifulSoup``) are needed
only if you use XML-like input or output formats.
However, since they are popular Python modules, to avoid complex import testing,
they are listed as requirements as they are imported
module-wise where they are used.

Depending on what ``aeneas`` classes you want to use,
you might need to install the following optional dependencies:

* ``requests`` (for using :class:`~aeneas.nuancettsapiwrapper.NuanceTTSAPIWrapper`)
* ``Pillow`` (for using :mod:`~aeneas.plotter`)
* ``youtube-dl`` and ``pafy`` (for using :class:`~aeneas.downloader.Downloader`)



Speeding Critical Sections Up: Python C Extensions
--------------------------------------------------

Forced alignment is a computationally demanding task,
both CPU-intensive and memory-intensive.
Aligning a dozen minutes of audio might require an hour
if done with pure Python code.

Hence, critical sections of the alignment code are written
as Python C extensions, that is, C code that receives input
from Python code, performs the heavy computation,
and returns results to the Python code.
The rule of thumb is that the C code only perform
"computation-like", low-level functions,
while "house-keeping", high-level functions
are done in Python land.

With this approach, aligning a dozen minutes of audio
requires only few seconds, and even aligning hours of audio
can be done in few minutes.
The drawback is that your environment must be able to compile
Python C extensions. If you install ``aeneas`` via ``PyPI``
(e.g., ``pip install aeneas``), the compilation step is done automatically for you.
Note that, due to the Python C extension compile and setup mechanism,
you must install ``numpy`` before installing ``aeneas``.

The Python C extensions included in ``aeneas`` are:

.. toctree::
    :maxdepth: 3

    cdtw
    cew
    cmfcc
    cwave

* :mod:`aeneas.cdtw`, for computing the DTW;
* :mod:`aeneas.cew`, for synthesizing text via the ``eSpeak`` C API;
* :mod:`aeneas.cmfcc`, for computing a MFCC representation of a WAVE (RIFF) audio file;
* :mod:`aeneas.cwave`, for reading WAVE (RIFF) audio files.

.. note::
    
    Currently :mod:`aeneas.cew` is available only on Linux,
    since compiling it on Mac OS X and Windows cannot be automated.
    However, starting from v1.5.0, the pure Python code
    for synthesizing text with eSpeak via ``subprocess``
    is only 2-3 times slower than :mod:`aeneas.cew`.
    Unless you work with thousands of text fragments,
    the performance difference is negligible.

.. note::
    
    Currently :mod:`aeneas.cwave` is not used.
    


Concepts
--------

Except for "enumeration" classes (e.g., :class:`~aeneas.textfile.TextFileFormat`) and
"data-only" classes (e.g., :class:`~aeneas.textfile.TextFragment`), most classes
are subclasses of :class:`~aeneas.logger.Loggable`,
which provides the ability to log events using a shared
:class:`~aeneas.logger.Logger` object (``logger``),
and to inject runtime execution parameters using a shared
:class:`~aeneas.runtimeconfiguration.RuntimeConfiguration` object (``rconf``).

The ``logger`` can tee (i.e., store messages and print them to stdout)
or dump to file.

The ``rconf`` provides a way to fine tune ``aeneas``
by changing its internal behavior.
The library defaults should fine for most use cases,
and they do not require explicitly passing an ``rconf`` object.

.. Topic:: Example

    Process a task with custom parameters, and log messages::    
    
        # create Logger which logs and tees
        logger = Logger(tee=True)

        # create RuntimeConfiguration object, with custom MFCC length and shift
        rconf = RuntimeConfiguration()
        rconf[RuntimeConfiguration.MFCC_WINDOW_LENGTH] = TimeValue(u"0.150")
        rconf[RuntimeConfiguration.MFCC_WINDOW_SHIFT] = TimeValue(u"0.050")

        # create Task object
        task = ...

        # process Task with custom parameters
        ExecuteTask(task, rconf=rconf, logger=logger).execute()

If you read from/write to file, you should be fine
interacting only with :class:`~aeneas.task.Task` functions.
For example, setting a path in
:func:`~aeneas.task.Task.audio_file_path_absolute`
(resp., :func:`~aeneas.task.Task.text_file_path_absolute`)
force the library to load the given file,
and to create a
:class:`~aeneas.audiofile.AudioFile`
(resp., :class:`~aeneas.textfile.TextFile`)
object behind the scenes, storing it inside the Task object.

However, you can also build e.g. your own
:class:`~aeneas.textfile.TextFile`
and then assign it to your Task.

.. Topic:: Example

    Create a TextFile programmatically, and assign it to Task::    

        task = Task()
        textfile = TextFile()
        for identifier, frag_text in [
            (u"f001", [u"first fragment"]),
            (u"f002", [u"second fragment"]),
            (u"f003", [u"third fragment"])
        ]:
            textfile.add_fragment(TextFragment(identifier, Language.ENG, frag_text, frag_text))
        task.text_file = textfile

Starting with v1.5.0, both :class:`~aeneas.textfile.TextFile`
and :class:`~aeneas.syncmap.SyncMap` are backed by the
:class:`~aeneas.tree.Tree` structure, which can represent multilevel I/O files.
Both have a "virtual" (empty) root node, to which the "level 1" nodes
are attached.
Note that single-level text files and sync maps are a special case,
where only "level 1" nodes are present, producing a tree with a root node
and a list of children, effectively equivalent to the "list" structure pre-v1.5.0.



Miscellanea
-----------

* Ensuring that all the strings you pass to ``aeneas`` are Unicode strings
  will save you a lot of headaches.
  If you read from files, be sure they are encoded using ``UTF-8``.
* You can use any audio file format that is supported by ``ffprobe`` and ``ffmpeg``.
  If unsure, just try them on your audio file on the console:
  if it works there, it should work inside ``aeneas`` too.
* Enumeration classes usually have an ``ALLOWED_VALUE`` class member,
  which lists all the allowed values. For example:
  :data:`~aeneas.textfile.TextFileFormat.ALLOWED_VALUES`.
  This list is used for example by the validator to check input values.
* Most classes are optimized for reducing memory consumption.
  For example, if you create an :class:`~aeneas.audiofilemfcc.AudioFileMFCC`
  with a file path, the input audio file will be converted to a temporary WAVE file,
  audio samples will be read into memory, MFCCs will be computed,
  and then audio data will be discarded from memory and the temporary WAVE file
  will be deleted, keeping only the MFCC matrix into memory.
  If you prefer persistence, you need to build intermediate objects yourself
  (i.e., :class:`~aeneas.ffmpegwrapper.FFMPEGWrapper`,
  :class:`~aeneas.audiofile.AudioFile`, etc.)
  and properly dispose of them in your code.
* Wherever possible, ``NumPy`` views are used to avoid data copying.
  Similarly, built-in ``NumPy`` functions are used to improve run time. 
* To avoid numerical issues, always use :class:`~aeneas.timevalue.TimeValue`
  to hold time values with arbitrary precision.
  Note that doing so incurs in a negligible execution slow down,
  because the heaviest computations are done with integer ``NumPy`` indices and arrays
  and the transformation to :class:`~aeneas.timevalue.TimeValue` takes place
  only when the sync map is output to file.



Module ``aeneas``
~~~~~~~~~~~~~~~~~

The main ``aeneas`` module contains several subpackages:

* :mod:`aeneas.cdtw` (Python C extension)
* :mod:`aeneas.cew` (Python C extension)
* :mod:`aeneas.cmfcc` (Python C extension)
* :mod:`aeneas.cwave` (Python C extension)
* :mod:`aeneas.extra`
* :mod:`aeneas.tests`
* :mod:`aeneas.tools`

and the following modules:

.. toctree::
    :maxdepth: 3

    adjustboundaryalgorithm
    analyzecontainer
    audiofile
    audiofilemfcc
    cewsubprocess
    configuration
    container
    diagnostics
    downloader
    dtw
    espeakwrapper
    executejob
    executetask
    festivalwrapper
    ffmpegwrapper
    ffprobewrapper
    globalconstants
    globalfunctions
    hierarchytype
    idsortingalgorithm
    job
    language
    logger
    mfcc
    nuancettsapiwrapper
    plotter
    runtimeconfiguration
    sd
    syncmap
    synthesizer
    task
    textfile
    timevalue
    ttswrapper
    vad
    validator



Module ``aeneas.extra``
~~~~~~~~~~~~~~~~~~~~~~~

The ``aeneas.extra`` module contains some extra Python source files
which provide **experimental** and **not officially supported** functions,
mainly custom, not built-in TTS engine wrappers.

For example, if you want to write your own custom TTS engine wrapper,
have a look at the ``aeneas/extra/ctw_espeak.py`` source file,
which is heavily commented and should be easy to modify for your own TTS engine.



Module ``aeneas.tests``
~~~~~~~~~~~~~~~~~~~~~~~

The ``aeneas.tests`` module contains the **unit test** files for ``aeneas``.

Resources needed to run the tests,
for example audio and text files,
are located in the ``aeneas/tests/res/`` directory.



.. _libtutorial_tools:

Module ``aeneas.tools``
~~~~~~~~~~~~~~~~~~~~~~~

The ``aeneas.tools`` module contains the built-in command line tools for ``aeneas``.

The two main tools are:

* ``aeneas.tools.execute_job``
* ``aeneas.tools.execute_task``

which are described in the :ref:`clitutorial`.

Moreover, the ``aeneas.tools`` module also contains the following programs,
useful for debugging or converting between different file formats:

* ``aeneas.tools.convert_syncmap``: convert a sync map from a format to another
* ``aeneas.tools.download``: download a file from a Web resource (currently, audio from a YouTube video)
* ``aeneas.tools.extract_mfcc``: extract MFCCs from a monoaural WAVE file
* ``aeneas.tools.ffmpeg_wrapper``: a wrapper around ``ffmpeg``
* ``aeneas.tools.ffprobe_wrapper``: a wrapper around ``ffprobe``
* ``aeneas.tools.plot_waveform``: plot a waveform and sets of labels to file
* ``aeneas.tools.read_audio``: read the properties of an audio file
* ``aeneas.tools.read_text``: read a text file and show the extracted text fragments
* ``aeneas.tools.run_sd``: read an audio file and the corresponding text file and detect the audio head/tail
* ``aeneas.tools.run_vad``: read an audio file and compute speech/nonspeech time intervals
* ``aeneas.tools.synthesize_text``: synthesize several text fragments read from file into a single wav file
* ``aeneas.tools.validate``: validate a job container or configuration strings/files

Run each program without arguments
to get its help manual and usage examples.

Resources needed to run the live examples,
for example audio and text files,
are located in the ``aeneas/tools/res/`` directory.



