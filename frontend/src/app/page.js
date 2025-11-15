'use client';

import AppHeader from "../components/app/app-header/app-header.jsx";
import Hero from "../components/hero/hero.jsx";
import Workflow from "../components/workflow/workflow.jsx";
import About from "../components/about/about.jsx";
import Contact from "../components/contact/contact.jsx";

export default function Home() {
  return (
    <main>
      <AppHeader />

      {/* HERO */}
      <Hero />

      {/* ABOUT THE PLATFORM */}
      <About />

      {/* WHAT THE PLATFORM DOES */}
      <Workflow />

      <Contact />

    </main>



  );
}
