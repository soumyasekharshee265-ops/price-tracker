import { motion } from 'framer-motion';

function Mascot({ size = 90, className = '' }) {
  return (
    <motion.div
      className={`mascot ${className}`}
      style={{ width: size, height: size }}
      animate={{ y: [0, -10, 0] }}
      transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut' }}
    >
      <svg viewBox="0 0 120 120" width="100%" height="100%">
        {/* Propeller */}
        <g className="mascot-propeller">
          <rect x="52" y="6" width="16" height="4" rx="2" fill="#f0c419" />
          <circle cx="60" cy="14" r="4" fill="#8b5cf6" />
        </g>
        <line x1="60" y1="14" x2="60" y2="24" stroke="#8b5cf6" strokeWidth="3" />

        {/* Head */}
        <circle cx="60" cy="55" r="34" fill="#38bdf8" />
        <circle cx="60" cy="58" r="27" fill="#f5f7ff" />

        {/* Ears */}
        <circle cx="38" cy="34" r="10" fill="#38bdf8" />
        <circle cx="82" cy="34" r="10" fill="#38bdf8" />

        {/* Eyes */}
        <circle cx="48" cy="56" r="6" fill="#141a28" />
        <circle cx="72" cy="56" r="6" fill="#141a28" />
        <circle cx="50" cy="54" r="1.8" fill="#f5f7ff" />
        <circle cx="74" cy="54" r="1.8" fill="#f5f7ff" />

        {/* Nose + mouth */}
        <circle cx="60" cy="66" r="2.5" fill="#f472b6" />
        <path d="M60 68 Q54 74 48 70" stroke="#141a28" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M60 68 Q66 74 72 70" stroke="#141a28" strokeWidth="2" fill="none" strokeLinecap="round" />

        {/* Whiskers */}
        <line x1="20" y1="58" x2="38" y2="60" stroke="#8b93a7" strokeWidth="1.5" />
        <line x1="20" y1="66" x2="38" y2="65" stroke="#8b93a7" strokeWidth="1.5" />
        <line x1="100" y1="58" x2="82" y2="60" stroke="#8b93a7" strokeWidth="1.5" />
        <line x1="100" y1="66" x2="82" y2="65" stroke="#8b93a7" strokeWidth="1.5" />
      </svg>
    </motion.div>
  );
}

export default Mascot;