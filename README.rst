InvokeAI Benchmark
==================

**InvokeAI-Benchmark** is a simple tool to evaluate performance of InvokeAI.

Install
-------

::

  pip install https://github.com/cloudmercato/invokeai-benchmark/archive/refs/heads/master.zip
  
  
Usage
-----

Command line
~~~~~~~~~~~~

Test example
~~~~~~~~~~~~

::

  $ invokeai-benchmark --api-url http://your-server:9090/api/v1/ -p "Large landscape of Dijon"
  batch_id : 809daf7d-d0a3-4066-a1df-74c2e530580f
  item_id : 151
  session_id : 5dfa456e-7f58-4c94-8fd9-2321c400dd31
  image_path : http://your-server:9090/api/v1/images/i/c6968dbe-f34a-4991-a07c-eeaf2157d9cb.png/full
  prompt : Large landscape of Dijon
  width : 512
  height : 512
  seed : 0
  cfg_scale : 7.5
  scheduler : euler
  steps : 50
  fp32 : True
  priority : 0
  error : None
  created_at : 2023-11-28 05:53:32.795
  started_at : 2023-11-28 05:53:32.804
  completed_at : 2023-11-28 05:53:42.510
  queue_elapsed : 0.009
  task_elapsed : 9.706
  total_elapsed : 9.715
  pixel_rate : 27008.448
  version : 3.4.0post2


Contribute
----------

This project is created with ❤️ for free by `Cloud Mercato`_ under BSD License. Feel free to contribute by submitting a pull request or an issue.

.. _`Cloud Mercato`: https://www.cloud-mercato.com/
