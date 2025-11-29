<template>
    <canvas ref="particleCanvas" class="particle-layer" :width="canvasWidth" :height="canvasHeight"></canvas>
</template>

<script>
export default {
    name: "ParticleLayer",
    data() {
        return {
            canvasWidth: window.innerWidth,
            canvasHeight: window.innerHeight,
            particles: [],
        };
    },
    mounted() {
        this.initParticles();
        window.addEventListener("resize", this.resizeHandler);
    },
    beforeDestroy() {
        window.removeEventListener("resize", this.resizeHandler);
    },
    methods: {
        resizeHandler() {
            this.canvasWidth = window.innerWidth;
            this.canvasHeight = window.innerHeight;
            const particleCanvas = this.$refs.particleCanvas;
            if (particleCanvas) {
                particleCanvas.width = this.canvasWidth;
                particleCanvas.height = this.canvasHeight;
            }
        },

        initParticles() {
            const canvas = this.$refs.particleCanvas;
            canvas.width = this.canvasWidth;
            canvas.height = this.canvasHeight;
            const ctx = canvas.getContext("2d");

            // 创建粒子数组
            this.particles = Array.from({ length: 200 }, () => ({
                x: Math.random() * this.canvasWidth,
                y: Math.random() * this.canvasHeight,
                vx: (Math.random() - 0.5) * 0.2,
                vy: Math.random() * 0.5 + 0.2,
                size: Math.random() * 2 + 1,
                alpha: Math.random() * 0.5 + 0.2,
            }));

            let lastTime = 0;
            const animateParticles = (timestamp) => {
                if (!lastTime) lastTime = timestamp;
                const deltaTime = timestamp - lastTime;
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                this.particles.forEach((p) => {
                    p.x += p.vx * deltaTime * 0.05;
                    p.y += p.vy * deltaTime * 0.05;
                    if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                    if (p.y > canvas.height) {
                        p.y = 0;
                        p.x = Math.random() * canvas.width;
                    }
                    ctx.beginPath();
                    ctx.fillStyle = `rgba(255,255,255,${p.alpha})`;
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                    ctx.fill();
                });
                lastTime = timestamp;
                if (document.visibilityState === "visible") {
                    requestAnimationFrame(animateParticles);
                }
            };
            requestAnimationFrame(animateParticles);
        },
    },
};
</script>

<style scoped>
.particle-layer {
    position: absolute;
    top: 0;
    left: 0;
    pointer-events: none;
    position: fixed;
    z-index: 1;
}
</style>