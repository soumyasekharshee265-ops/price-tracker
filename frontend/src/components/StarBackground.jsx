import { useEffect, useRef } from 'react';

function StarBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;


    const bigStars = Array.from({ length: 3 }, () => ({
      x: Math.random() * canvas.width * 0.4,
      y: Math.random() * canvas.height * 0.4,
      radius: Math.random() * 1 + 1.5,
      opacity: Math.random() * 0.5,
      speed: Math.random() * 0.015 + 0.004,
    }));

  
    const smallStars = Array.from({ length: 6 }, () => ({
      x: canvas.width * 0.35 + Math.random() * canvas.width * 0.65,
      y: canvas.height * 0.35 + Math.random() * canvas.height * 0.65,
      radius: Math.random() * 0.5 + 0.3,
      opacity: Math.random() * 0.35,
      speed: Math.random() * 0.015 + 0.004,
    }));

    const stars = [...bigStars, ...smallStars];

    let animationId;

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach((star) => {
        star.opacity += star.speed;
        if (star.opacity > 0.5 || star.opacity < 0) star.speed *= -1;

        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${Math.abs(star.opacity)})`;
        ctx.fill();
      });
      animationId = requestAnimationFrame(draw);
    }

    draw();

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
        pointerEvents: 'none',
      }}
    />
  );
}

export default StarBackground;