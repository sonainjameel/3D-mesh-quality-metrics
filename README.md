# 3D Objective Metrics for Semantic Mesh Distortion Analysis

This repository contains Python code used in our study on evaluating whether classical 3D geometric metrics can detect **semantic distortions** in human and animal meshes. The code computes three widely used objective measures between two 3D meshes:

- **Chamfer Distance (CD)**
- **Hausdorff Distance (HD)**
- **RMS Vertex Distance (Open3D)**

These metrics are evaluated to support our paper section:  
**“3D Objective Metrics”**  
used to generate the values in Table 1 of the paper.

---

## 🧩 Background & Motivation

Traditional geometric metrics capture local distance differences between surfaces, but **often fail to detect semantic or anatomical distortions**—such as extra fingers, stretched limbs, or rearranged joints.

Our study compares **human perceptual sensitivity** vs. **modern multimodal LLMs (ChatGPT-5, Gemini, Qwen MAX-3)** on pairs of subtly distorted meshes. Surprisingly:

- Humans showed clear sensitivity to distortions  
- ChatGPT-5 and Gemini answered *“Equal”* for all pairs  
- Qwen MAX-3 answered *one mesh always preferred*, regardless of distortion  
- Objective metrics (CD, HD, RMS) showed only small numerical differences

This highlights a core limitation: **current LLMs do not meaningfully perceive semantic 3D geometry**, and common 3D metrics also fail to reflect semantic degradation.

---

## 📄 Abstract (WACV Workshop)

Assessing the perceptual quality of 3D meshes remains a stubborn challenge: traditional geometric metrics often miss the very errors that people notice first. A human observer can immediately spot an extra finger, a stretched limb, or a misplaced joint. These semantic defects barely alter vertex distances and often go completely undetected by automated measures.

To explore whether modern large language models (LLMs) can help bridge this gap, we constructed a controlled set of human and animal meshes with subtle anatomical distortions and asked both human participants and state-of-the-art multimodal LLMs to choose which of two shapes they preferred. The results were unambiguous: humans were sensitive to distortions, while LLMs were not. ChatGPT-5 and Gemini answered *“Equal”* for every pair, and Qwen MAX-3 consistently selected the same mesh regardless of distortion.

Our findings show that today’s LLMs do not perceive semantic 3D geometry in any meaningful way. As 3D reconstruction and generative models become widespread, subtle semantic errors—including 3D deepfakes—underscore the need for tools beyond current multimodal LLMs for reliable, human-aligned mesh evaluation.

---

## 📦 Installation

```bash
pip install trimesh scipy numpy open3d scikit-learn
