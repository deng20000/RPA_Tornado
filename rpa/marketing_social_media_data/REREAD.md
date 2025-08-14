# 数据处理流程文字版预览（双主线）

---

## 钉钉多维表数据处理流程（仅输出 optimized_data_structure_update.json）

### 1. 输入文件
- `dingding_fields.json`：钉钉多维表所有字段信息
- `dingding_allfields.json`：钉钉多维表所有数据信息

### 2. 数据筛选
- 仅保留`时间`字段为昨天（YYYY.MM）的数据行

### 3. 提取基础信息
- 提取每条数据的`id`、`社媒账号`、`渠道`

### 4. available_fields 字段标准化
- `available_fields`字段内容严格如下：

#### FaceBook
- New Fans
- Posts Published
- Posts Impressions
- Posts Engagement
- Posts Reactions
- Posts Comments
- Posts Shares
- Posts Video Plays

#### Youtube
- Total Subscribers
- Subscribers Gained
- Engagement
- Views
- Post

#### Instagram
- Total Followers
- Total Interactions
- Total Views
- Total Reach
- Post Published

#### LinkedIn
- Total Followers-linkedin
- Total Posts
- Follower Growth
- Total Impressions
- Total Page Likes
- Total Page Clicks

#### X
- Followers
- Following
- Total Tweets

### 5. 结构优化与输出
- 推荐采用`fields_dict + records`结构：
  - 顶层有`fields_dict`（字段ID到字段名的全局唯一映射）
  - `records`下每条数据只存储字段ID与数值的对应关系（数值可为null或缺失）
  - 字段名和ID不冗余在最低层，所有字段名查找都通过`fields_dict`完成
- 输出文件为：`optimized_data_structure_update.json`
- 结构示例：

```json
{
  "fields_dict": {
    "field_id_1": "New Fans",
    "field_id_2": "Posts Published",
    "field_id_3": "Posts Impressions",
    "field_id_4": "Posts Engagement",
    "field_id_5": "Posts Reactions",
    "field_id_6": "Posts Comments",
    "field_id_7": "Posts Shares",
    "field_id_8": "Posts Video Plays",
    "field_id_9": "Total Subscribers"
    // ... 其它字段
  },
  "records": {
    "id1": {
      "basic_info": {
        "time": "2024.06",
        "social_account": "xxx",
        "channel": "FaceBook"
      },
      "fields": {
        "field_id_1": 123,
        "field_id_2": 10,
        "field_id_3": null,
        "field_id_4": 888
        // ... 其它字段
      }
    },
    "id2": {
      "basic_info": {
        "time": "2024.06",
        "social_account": "xxx",
        "channel": "Youtube"
      },
      "fields": {
        "field_id_9": 456
        // ... 其它字段
      }
    }
    // 其它平台同理
  }
}
```

---

- `optimized_data_structure_update.json`是唯一标准输出，且`available_fields`字段内容完全按最新指定的各平台字段列表。

## 根据多维表获取+不同网站源文件，更新多维表数据

1. **输入文件**
   - `optimized_data_structure_update.json`（由逻辑一生成的标准结构）
   - 各网站源数据文件（如`fb_fetch_inf.json`、`youtube_fetch_inf.json`等）

2. **解析网站源数据**
   - 结构化各网站原始数据，提取核心内容
   - 输出中间文件（如有需要）：如`fb_fetch_inf_update.json`等，仅供后续步骤使用

3. **字段自动映射**
   - 以中间文件为输入，进行字段自动/手动映射

4. **填充/更新多维表数据**
   - 将各网站数据按标准结构填充到多维表结构中

5. **生成映射报告**
   - 统计映射成功率、详细映射关系（如有需要）

6. **输出文件**
   
   （本流程无需额外输出文件，所有数据直接在`optimized_data_structure_update.json`中维护和更新）

--- 

### Facebook字段映射关系（前缀模糊匹配+jsonpath模板）

| 字段名            | fb_fetch_inf_update.json字段key前缀      | jsonpath模板                                               |
|-------------------|------------------------------------------|------------------------------------------------------------|
| New Fans          | fb-fans                                  | $.response[fb-fans*].count                                 |
| Posts Published   | fb-post-published                        | $.response[fb-post-published*].count                       |
| Posts Impressions | fb-post-impressions                      | $.response[fb-post-impressions*].count                     |
| Posts Engagement  | fb-post-engagement                       | $.response[fb-post-engagement*].count                      |
| Posts Reactions   | fb-posts-reaction                        | $.response[fb-posts-reaction*].count                       |
| Posts Comments    | fb-post-comments-count                    | $.response[fb-post-comments-count*].count                  |
| Posts Shares      | fb-post-shares                           | $.response[fb-post-shares*].count                          |
| Posts Video Plays | fb-post-video-views                      | $.response[fb-post-video-views*].count                     |

说明：
- 字段key前缀为fb_fetch_inf_update.json中response下以该前缀开头的所有key。
- jsonpath模板中的*表示模糊匹配，实际使用时需遍历所有以该前缀开头的key。
- 其它平台可参照此方式补充映射关系。 