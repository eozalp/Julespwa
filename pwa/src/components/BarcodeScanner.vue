<template>
  <div class="barcode-scanner">
    <video ref="video" autoplay playsinline></video>
    <div v-if="isScanning" class="overlay">
      <div class="laser"></div>
    </div>
    <button @click="toggleScan">{{ isScanning ? 'Stop' : 'Start' }} Scanning</button>
  </div>
</template>

<script>
export default {
  name: 'BarcodeScanner',
  data() {
    return {
      isScanning: false,
      stream: null,
      lastScanned: null,
      lastScannedTime: 0,
      beep: null,
    };
  },
  mounted() {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
  },
  methods: {
    async toggleScan() {
      if (this.isScanning) {
        this.stopScan();
      } else {
        await this.startScan();
      }
    },
    async startScan() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        });
        this.$refs.video.srcObject = this.stream;
        this.isScanning = true;
        this.scanLoop();
      } catch (err) {
        console.error("Error accessing camera:", err);
        alert("Could not access the camera. Please ensure you have given permission.");
      }
    },
    stopScan() {
      this.isScanning = false;
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
      }
    },
    async scanLoop() {
      if (!this.isScanning) return;

      if (this.$refs.video.readyState === this.$refs.video.HAVE_ENOUGH_DATA) {
        if ('BarcodeDetector' in window) {
          await this.detectWithNativeAPI();
        } else {
          await this.detectWithJsQR();
        }
      }

      requestAnimationFrame(this.scanLoop);
    },
    async detectWithNativeAPI() {
      try {
        const barcodeDetector = new window.BarcodeDetector({ formats: ['ean_13', 'upc_a', 'code_128'] });
        const barcodes = await barcodeDetector.detect(this.$refs.video);
        if (barcodes.length > 0) {
          this.processBarcode(barcodes[0].rawValue);
        }
      } catch (err) {
        console.error("BarcodeDetector error:", err);
      }
    },
    async detectWithJsQR() {
      if (!this.canvas) {
        this.canvas = document.createElement('canvas');
      }
      const video = this.$refs.video;
      this.canvas.width = video.videoWidth;
      this.canvas.height = video.videoHeight;
      const ctx = this.canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, this.canvas.width, this.canvas.height);
      const imageData = ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);

      const jsQR = (await import('jsqr')).default;
      const code = jsQR(imageData.data, imageData.width, imageData.height, {
        inversionAttempts: "dontInvert",
      });

      if (code) {
        this.processBarcode(code.data);
      }
    },
    processBarcode(barcodeValue) {
      const now = Date.now();
      if (barcodeValue === this.lastScanned && now - this.lastScannedTime < 3000) {
        // Debounce: ignore if the same barcode is scanned within 3 seconds
        return;
      }

      this.lastScanned = barcodeValue;
      this.lastScannedTime = now;

      this.provideFeedback();
      this.$emit('barcode-scanned', barcodeValue);
    },
    provideFeedback() {
      // Haptic feedback
      if ('vibrate' in navigator) {
        navigator.vibrate(200);
      }

      // Audible feedback
      if (this.audioContext) {
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        oscillator.frequency.value = 880; // A5 note
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
        gainNode.gain.linearRampToValueAtTime(0.5, this.audioContext.currentTime + 0.05);

        oscillator.start(this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.00001, this.audioContext.currentTime + 0.2);
        oscillator.stop(this.audioContext.currentTime + 0.2);
      }
    }
  }
};
</script>

<style scoped>
.barcode-scanner {
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: auto;
}
video {
  width: 100%;
  height: auto;
  border-radius: 8px;
}
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.laser {
  width: 80%;
  height: 2px;
  background-color: red;
  box-shadow: 0 0 5px red;
}
</style>
