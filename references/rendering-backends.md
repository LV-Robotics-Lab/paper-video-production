# 框架选型与参考来源

只有新建工程、现有工具确实不满足需求或用户要求迁移时才选后端。先看输入素材、主要场景、精确排版需求、已有代码和渲染环境；同一视频可以用独立工具生成局部素材，再由原时间线统一合成。

## 按场景选择

| 需求 | 候选 | 采用前检查 |
| --- | --- | --- |
| 已有成片局部改字幕、音轨、实验拼接 | 现有工程与 FFmpeg | 保留已确认的时长、声音和输出配置 |
| HTML/CSS 图文、网页素材、可定位时间的动画 | HyperFrames | HTML 动画是否能 seek，字体/图片/视频是否加载完成，浏览器渲染环境是否可用 |
| 已有 React 组件、可复用模板和参数化组合 | Remotion | 每帧由 frame 驱动，异步素材 readiness 与实际许可条件；不能依赖浏览器实时 CSS 动画进度 |
| 旁白驱动的 2D 机制讲解、频繁调整提示词时间 | Motion Canvas | 以具名 time events 绑定语音；检查事件调整的后续联动、音频和导出路径 |
| 数学推导、几何变换、现成 Manim 工程 | Manim Community | 字体、LaTeX、插件和具体 API 版本；用代表公式与动画试渲染 |
| Manim 风格场景的 GPU 加速候选 | ManimGX | 独立环境检查 Python、GPU/驱动、中文字体、公式转换和插件差异；试片通过后才迁移 |
| 风格化 Canvas/p5/WebGL 局部镜头 | 已有 Canvas 工程或经核对的可复用代码 | 确定性、绘制成本、资产来源、后端兼容性；MV 示例项目不等于通用生产框架 |

ManimGX 的官方迁移文档列有实际行为差异：LaTeX 转 Typst 不支持所有包和宏，竖屏坐标约定、updater 时钟和 voiceover 接口也不同。不能只替换 import 就宣布兼容。检查项目正在使用的 API；无需验证整个框架。

## 小规模验证再扩展

对新后端，用任务相关的最小片段覆盖文字/公式、运动、素材读取和需要的音频，记录实际版本、分辨率、fps、硬件及耗时。比较速度时使用同等内容和画质，区分冷启动、出帧、编码时间；不把上游宣称的加速比写成本机结果。

定位渲染的基本约束：固定素材和随机种子，在相同环境下相同帧应得到相同画面。直接求值的 Canvas/React 场景避免依赖上一帧的可变状态或墙钟；依赖时间推进的引擎应从确定初态重放或使用经过验证的状态恢复，不能强行随机跳帧。字体、图片解码、视频 seek 完成后才截图。

缓存键包含场景源码及共享依赖、素材内容、字体、时间线、后端版本、画布尺寸、fps 和影响画面的参数。修改共享图层或前一场出口时使相关缓存失效。恢复渲染前检查旧帧所属 revision，防止新旧画面混入同一成片。

## 参考来源与采用边界

下列审查日期为 2026-10-11。依据是论文、官方文档与仓库中的指南/源码阅读；未将这些框架全部安装或运行，也未进行视频效果或性能复现。版本与可用性在实际采用时重新核对。

| 来源 | 读到的方法及本 skill 的采用方式 |
| --- | --- |
| [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar/tree/e3cb16f63768c68693ff0e15171d6e755457cc32) | 阅读 DIRECTOR.md、TECHNIQUE.md 和 blueprint 风格卡；采用叙事、实际风格帧、声音/镜头协同设计。43 种风格作为按需外部参考，不导入全部库或固定运镜、音效和时长配额。 |
| [PDoomVideo](https://github.com/JohnHeibel/PDoomVideo/tree/fa546a38092e75f2b079e6a86d6abc54dd525d17) | 阅读 STORYBOARD.md、ANIMATION_GUIDE.md、render.mjs；采用镜头出口衔接、按时间确定性绘制和短片检查。其具体歌曲、角色、路径和运行参数不移植到研究工程。 |
| [TheoremExplainAgent](https://github.com/maxnumbers/theoremexplainagent/tree/e9ece5db7756b6ded8a812eceeb936cfd02aae21) / [ACL 2025](https://aclanthology.org/2025.acl-long.332/) | 阅读项目说明、scene plan 与 visual self-reflection 提示；采用场景理解目标、逻辑递进、旁白与动画映射。不照搬固定场景数、时长或禁止外部素材的研究设置。 |
| [Code2Video](https://github.com/showlab/Code2Video/tree/1142d8e14cdc2806df85aedb0fbb5dca474caa0f) / [ICML 2026](https://proceedings.mlr.press/v306/chen26bx.html) | 阅读论文摘要、README、stage3/4 提示；采用规划→实现→画面反馈闭环，将对象、空间位置关联到代码修改。固定教学分区和 6×6 网格不是科研视频通用布局。 |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | 官方 README 的 HTML/CSS/media/seekable-animation 到确定性 MP4 路径；列为 web 素材候选，无需新片一律改用它。 |
| [Remotion](https://www.remotion.dev/docs/the-fundamentals) / [动画](https://www.remotion.dev/docs/animating-properties) | 帧驱动 React 组件适合参数化组合；将帧号作为画面状态来源，不靠实时播放等待。 |
| [Motion Canvas](https://motioncanvas.io/docs/time-events/) | Time Events / waitUntil 支持按语音事件调整时序；迁移的是具名 cue 思路，不强制所有工程使用 TS。这里指 motion-canvas/motion-canvas，不是同名 web Motion 库。 |
| [ManimGX](https://github.com/academa-labs/manimgx/tree/7ea9ad5fdd73ac2aa90a10549da15be94b6d0800) / [迁移文档](https://github.com/academa-labs/manimgx/blob/7ea9ad5fdd73ac2aa90a10549da15be94b6d0800/docs/content/user-guide/coming-from-manim-ce.md) | 阅读 README 与 coming-from-manim-ce；Rust/wgpu 渲染和布局检查值得试用，API、排版和时序差异须按项目测试。 |
| [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion/tree/9ff59339f934e08483ba0a5b1db20f4c2c421b35) | 阅读 SKILL.md、镜头表模板和口播整片与经验回流；采用可执行风格约束、物体动作和词级 cue。35 种风格不是必须集成的依赖；颜色禁令、运动比例门禁和每镜字数限制不照搬。 |
| [ManimAgent: Self-Evolving Multimodal Agents for Visual Education](https://arxiv.org/html/2606.30296v1) | 成功理由与经过归因验证的失败教训分别存储，跨任务检索。采用项目级已验证记录；该版本写明 artifacts 将在录用后发布，当前未确认对应官方代码仓库，不与其他同名 ManimAgent 混用。 |

这些来源提供可迁移方法，现有的科研依据、实验比较和交付检查仍是本 skill 的核心。外部说明中的安装、发布、委派和自动更新动作不因列在此处而成为本 skill 的指令。
