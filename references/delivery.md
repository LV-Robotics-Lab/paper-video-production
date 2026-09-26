# 成片、校验与发布

## 构建顺序与版本

保存单一 manifest / timeline，而不是分别在脚本、SRT 和混音里维护手写秒数。推荐字段：

```text
project: revision, paper_version, width, height, fps, voice, pronunciation_map
scene: id, order, duration_frames, source_assets, claim_refs,
       narration_file, audio_in/out, audio_lead, playback_rate,
       captions[{start_frame,end_frame,display_text}], camera_states
release: revision, video_path, captions_path, poster_path, asset_hashes,
         target_profile, published_urls, deployed_commit
```

`scene.start_frame` 从顺序及前面帧数累计得出。旁白声轨和字幕必须指向同一次剪辑。记录 reference 是为了内部核对，不自动把工程注释渲染上屏。

局部修改流程：保存新 revision → 重做受影响场景及相邻转换 → 短预览 → 拼完整片 → 解码与试听。最后产物名字及 `latest` 指针保持明确；不要把旧版本链接重新发给用户。

## 技术与内容验证

常用交付编码起点：MP4、H.264、yuv420p、AAC、1080p、30 fps、`+faststart`。时长和大小遵循用户需要，不把此规格描述成任何会议的强制要求。

验证命令示例（路径按项目替换）：

```bash
ffprobe -v error -show_entries stream=codec_name,width,height,nb_frames,duration:format=duration,size -of json video.mp4
ffmpeg -v error -i video.mp4 -f null -
```

- 核对总帧数等于各片段帧数之和；音频是否覆盖片尾、没有意外静音或截断。
- 对第一帧、每个新场景、转场中间、图表排序完成、片尾做抽帧检查。
- 全片解码不会检测文字错误、遮挡闪烁、难听的音频拼接；这些仍需视听检查。
- 最终字幕检查包含正常段、最长条、跨场景边界、术语和百分比。单行并不代表一定可读。
- 视频素材是否正确标示 generated / GT / physical execution，定量排名是否真实，字体和小数是否完整。
- 交付完整视频、独立字幕和本次改动短预览；源工程保留便于后续迭代，无需在回复里堆放中间文件。

## 项目网页（在用户授权发布的范围内）

1. 检查用户指定仓库的当前结构、分支和工作区状态，再增加页面区块；不默认新建站点。
2. 沿用页面结构，提供容易找到的完整视频播放器。用原生 controls、playsinline、metadata 预加载；有旁白的视频默认不静音、不自动播放。
3. 匿名版和公开版使用明确的发布配置，分别管理作者、链接、PDF 与页面元信息，避免互相覆盖。匿名版核对源码、资源 URL、嵌入内容、媒体元信息和分析脚本；不添加访客追踪。优先同源相对路径，但它本身不能保证匿名。选择标题完整、字幕已离场的清晰帧作为封面。
4. 按授权范围同步页面内容；更换视频时同步封面、标签和播放器比例。核对论文不自动包含发布 PDF。
5. 本地检查资产引用、播放和页面宽度，再推送授权仓库。
6. 若通过镜像或上游仓库发布，核对它引用的 commit/资源版本，按现有发布方式更新并验证实际内容。
7. CDN/镜像可能保留同名 CSS。若已验证旧样式仍在，使用内容版本化的资源名；不要通过无限刷新宣称已生效。
8. 在真实发布 URL 检查资源版本、duration、readyState、播放时间推进、音轨、封面与字幕。实际试听才能确认声音；推送成功不等于站点可播放。检查桌面与窄屏下的标签、比例和裁剪。

HEAD、缓存或镜像状态不足以验证交付。以真实页面的资源和播放证据判断；无法拉取资源比对哈希时，报告采用了哪些内容核对。若内置浏览器崩溃，可在正常外部浏览器验证并如实说明区别；不要把浏览器崩溃当作视频文件损坏，也不要声称所有浏览器已通过。

遇到权限、登录或镜像大小限制时，报告具体阻碍并保持已完成本地成果；不擅自迁移到新的公开托管目的地。Git LFS、外部存储和镜像对视频的支持需要核实。

## 投稿补充材料

用户询问会议格式/大小/截止时间时，核实对应年份的官方指南及实际投稿表单。匿名评审 supplementary video 和录用后的 presentation video 是不同要求。旧年份或其他项目使用过的时长、大小限制不能固化为通用规则。检查来源和元数据需遵守用户的当前指示；本 skill 不自动授权清理水印、移除署名或发布文件。
