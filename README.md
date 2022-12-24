
## Demystify RAM Usage in Multi-Process Data Loaders

A typical PyTorch training program on 8 GPUs with 4 dataloader workers per GPU would create at least
`8 * (4+1) = 40` processes.
A naive use of torch dataset and dataloader can easily __replicate your dataset's RAM usage by 40 times__.
This issue has probably affected everyone who has done anything nontrivial with PyTorch.

[This blog post](https://ppwwyyxx.com/blog/2022/Demystify-RAM-Usage-in-Multiprocess-DataLoader/)
explains why it happens, and how to avoid the 40x RAM usage.

This github repo contains code and results for the above article.

### Dependencies
* PyTorch
* [psutil](https://github.com/giampaolo/psutil): `pip install psutil`
* Detectron2 for `main-multigpu*.py`: [installation from source](https://detectron2.readthedocs.io/en/latest/tutorials/install.html#build-detectron2-from-source) is required.
