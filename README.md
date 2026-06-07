# embedding_intro 使用说明

该项目包含 `embedding_intro.py`，使用 `sentence-transformers` 将中文句子转换为向量并计算余弦相似度。

推荐步骤（Windows PowerShell）：

1. 创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. 安装依赖：

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. 运行脚本：

```powershell
python embedding_intro.py
```

如果你使用 `conda`：

```powershell
conda create -n embed python=3.10 -y
conda activate embed
pip install -r requirements.txt
python embedding_intro.py
```

注意：某些系统（如受管理的 Python 安装）不允许在全局环境安装包，请使用虚拟环境或 conda 环境。