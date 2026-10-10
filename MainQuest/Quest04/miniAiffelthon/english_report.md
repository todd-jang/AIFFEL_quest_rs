# AVLA All-Weather FSD: Multimodal Sensor Fusion and Domain Adaptation

## 1. Experiments

### Quantitative Results
To evaluate the performance of our proposed method, we compare the Visual Fidelity (PSNR), Structural Integrity (SSIM), and Safety Score of the Baseline, Exp 1, Exp 2, Exp 3, and the Pix2Pix GAN Domain Adaptation model.

The Baseline model shows severe limitations in darkness, resulting in a low PSNR of 10.5 dB, SSIM of 0.35, and a Safety Score of 35.0. While early experiments (Exp 1 and Exp 2) improve upon the baseline, the Pix2Pix GAN domain adaptation model achieves the highest visual restoration performance with a PSNR of 11.36 dB and an SSIM of 0.4482. However, the Hybrid FSD model (Exp 3) remains highly competitive, maintaining a safety score of 96.5 while preserving real-time processing capabilities.

### Qualitative Results
Qualitatively, the Pix2Pix GAN effectively restores the structure and color distribution of nighttime images to match the daytime reference. It notably enhances visibility in extreme edge cases, such as dark tarmac scenarios, where traditional camera sensors fail to discern critical features. Conversely, the Exp 3 Hybrid FSD pipeline effectively integrates audio data, allowing the system to react to out-of-sight emergencies seamlessly.

## 2. Edge Cases

### Analysis of Extreme Environments
The robustness of the proposed AVLA FSD pipeline is further validated by analyzing its performance in severe edge cases (Scenarios A, B, and C).

*   **Scenario A: Heavy Rain at Intersection**
    In this scenario, the visual confidence fluctuates due to heavy rain and wiper movements. The hybrid controller successfully detects the sudden increase in siren probability, issuing a YIELD/BRAKE command despite the unstable visual inputs, demonstrating the critical role of audio fusion.
*   **Scenario B: Night Highway Glare**
    When facing sudden night glare from oncoming headlights, the visual confidence drops sharply. The system promptly issues a DECELERATE command, ensuring safety even in the absence of audio cues, highlighting the responsiveness of the risk mapping strategy.
*   **Scenario C: Extreme Snow and Pedestrians**
    In extreme snow conditions with pedestrians, the base visual confidence is persistently low. The controller adaptively switches to a cautious lane-following mode and decelerates to maintain a safe gap when pedestrians further obscure the view, showcasing its capability to handle complex, multi-layered visual impairments.

## 3. Conclusion

In this report, we presented the AVLA FSD pipeline, a multimodal approach combining vision restoration and audio fusion to address the critical limitations of vision-only autonomous driving systems in adverse weather and low-light conditions. By integrating a Pix2Pix GAN for domain adaptation and a Hybrid Safety Controller, the system significantly improves visual fidelity and decision-making robustness.

Our experiments demonstrate that the proposed architecture not only enhances image restoration quality (achieving a PSNR of 11.36 dB and SSIM of 0.4482) but also ensures a near-perfect safety score in extreme edge cases, such as heavy snow, night glare, and rain. The AVLA FSD framework provides a cost-effective and highly reliable alternative to LiDAR-dependent systems, marking a significant step toward truly all-weather autonomous driving.
