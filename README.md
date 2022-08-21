# qq_helper
观察到QQ等腾讯系的产品在运行过程中，会在后台发送用户行为数据，以方便腾讯的开发者更好地统计用户的行为习惯。本项目旨在帮助此类产品发送统计信息，让腾讯在短时间内接收到大量的多样化数据，从而提高腾讯开发者搜集数据的效率，进而帮助腾讯更好地了解用户行为习惯，改善其产品质量。

使用方法：

- 利用Github Actions
  - fork本项目，并在设置中允许actions运行即可
  - 由于免费用户使用actions有时长限制，因此本项目的默认配置是每小时运行30秒，用户可根据自己的账号情况修改`.github/workflows/post.yml`和`main_action.py`
- 在本地或自己的服务器上运行
  - 执行以下代码即可开始享受：

```bash
git clone https://github.com/tsuzcx/qq_helper
cd qq_helper
pip3 install -r requirements.txt
python3 main_local.py
```
