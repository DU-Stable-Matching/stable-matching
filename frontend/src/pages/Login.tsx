import React from "react";
import TopBar from "../components/TopBar.tsx";
import Footer from "../components/Footer.tsx";
import LoginHero from "../components/LoginHero.tsx";
import FAQ from "../components/FAQ.tsx";
import { useUserStore } from "../userState.ts";

const Login = () => {
  return (
    <>
      <TopBar />
      <LoginHero />
      <FAQ />
      <Footer />
    </>
  );
};

export default Login;
