import React from 'react'
import BackgroundCanvas from './BackgroundCanvas'
import FloatingComputer from './FloatingComputer'
import TrustedBy from './TrustedBy'

function LowerHome() {
  return (
    <div className="relative w-full h-full">
      {/* Background directly behind FloatingComputer */}
      <div className="absolute top-0 left-0 w-full h-full -z-10">
        <BackgroundCanvas />
      </div>

      {/* Foreground content */}
      <div className="relative z-10">
        <FloatingComputer />
        <TrustedBy />
      </div>
    </div>
  );
}

export default LowerHome
