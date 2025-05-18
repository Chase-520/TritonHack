import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#Chatgpt prompt used: using simulated ECG data create a program that uses Heart Rate Variability (HRV) to determine weather the user is having a panic attack

class ECGSimulator:
    def __init__(self, rr_intervals=None, rr_count=10, sampling_rate=1000):
        self.rr_count = rr_count
        self.sampling_rate = sampling_rate

        self.rr_intervals = rr_intervals
        self.time = None
        self.ecg_signal = None
        self.peaks = None
        self.rr_from_ecg = None
        self.anxiety_detected = None

    def generate_random_rr_intervals(self, anxious=False):
        """
        Generate synthetic RR intervals for simulating ECG.
        """
        base_rr = 0.45 if anxious else 0.8
        variability = 0.015 if anxious else 0.05
        rr_intervals = np.random.normal(loc=base_rr, scale=variability, size=self.rr_count)
        rr_intervals = np.clip(rr_intervals, 0.3, 1.5)
        self.rr_intervals = rr_intervals

    def simulate_ecg_waveform(self):
        """
        Simulates ECG waveform using RR intervals.
        """
        ecg = []
        time = []
        current_time = 0

        for rr in self.rr_intervals:
            beat_samples = int(rr * self.sampling_rate)
            t = np.linspace(0, rr, beat_samples)
            waveform = np.exp(-((t - rr / 3) ** 2) / (2 * 0.01 ** 2))
            waveform += np.random.normal(0, 0.01, size=beat_samples)
            ecg.extend(waveform)
            time.extend(t + current_time)
            current_time += rr

        self.time = np.array(time)
        self.ecg_signal = np.array(ecg)

    def extract_rr_intervals_from_ecg(self):
        peaks, _ = find_peaks(self.ecg_signal, height=0.6, distance=0.3 * self.sampling_rate)
        peak_times = self.time[peaks]
        self.rr_from_ecg = np.diff(peak_times)
        self.peaks = peaks

    def detect_anxiety(self, hr_threshold=100, hrv_threshold=0.05):
        if self.rr_from_ecg is None or len(self.rr_from_ecg) < 2:
            self.anxiety_detected = False
            return

        avg_rr = np.mean(self.rr_from_ecg)
        heart_rate = 60 / avg_rr
        hrv = np.std(self.rr_from_ecg)

        print("Detected from ECG signal:")
        print(f"  Avg Heart Rate: {heart_rate:.1f} bpm")
        print(f"  HRV (Std Dev of RR): {hrv:.4f} s")

        self.anxiety_detected = heart_rate > hr_threshold and hrv < hrv_threshold

    def plot_ecg(self):
        plt.figure(figsize=(12, 4))
        plt.plot(self.time, self.ecg_signal, label="ECG Signal")
        plt.plot(self.time[self.peaks], self.ecg_signal[self.peaks], 'ro', label="R-peaks")
        title = "ECG Analysis - " + ("Anxiety Detected" if self.anxiety_detected else "Normal")
        plt.title(title)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def run_analysis(self):
        if self.rr_intervals is None:
            raise ValueError("RR intervals not provided. Use generate_random_rr_intervals() or supply real RR intervals.")

        self.simulate_ecg_waveform()
        self.extract_rr_intervals_from_ecg()
        self.detect_anxiety()
        result = "⚠️  Anxiety Detected!" if self.anxiety_detected else "✅  No Anxiety Detected."
        print(result)
        self.plot_ecg()


# --- Usage Example ---

if __name__ == "__main__":
    sim = ECGSimulator(rr_count=12)
    
    # Create ECG from unknown mental state (try both for testing)
    sim.generate_random_rr_intervals(anxious=np.random.rand() > 0.5)

    # Analyze and determine if anxiety is present
    sim.run_analysis()
