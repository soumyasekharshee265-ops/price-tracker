import { motion } from 'framer-motion';
import Mascot from './Mascot';


const FLIGHT_PATH = {
  x: ['5vw', '85vw', '70vw', '15vw', '5vw'],
  y: ['10vh', '20vh', '70vh', '55vh', '10vh'],
};

function FlyingMascot() {
  return (
    <motion.div
      className="flying-mascot"
      animate={FLIGHT_PATH}
      transition={{ duration: 40, repeat: Infinity, ease: 'linear' }}
    >
      <Mascot size={60} />
    </motion.div>
  );
}

export default FlyingMascot;