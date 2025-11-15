export default function Home() {
  return (
    <main>
      {/* HERO */}
      <section className="hero">
        <div className="container">
          <h1>A Voice Platform <br></br> for Institutional Tasks</h1>
          <h2>Completed by Older Adults Through AR4U</h2>

          <p>
            <em>Surveys. Public‑service feedback. Clarity checks. Cultural micro‑stories.</em><br />
            All delivered via adaptive, safe phone interactions.<br />
            No digital barriers. No audio stored.
          </p>

          <a href="/dashboard" className="button-primary">
            Go to Researcher Portal
          </a>
        </div>
      </section>

      {/* WHAT THE PLATFORM DOES */}
      <section className="section-accent">
        <div className="container-wide">
          <h2>WHAT THE PLATFORM DOES</h2>
          <h3>Turn Institutional Text into Voice Tasks</h3>

          <p>
            We transform official surveys, service evaluations, clarity tests and cultural assignments
            into structured voice dialogues. Delivered entirely through <strong>AR4U</strong>, a trusted
            voice companion already used by older adults.
          </p>

          <h4>Supported task types</h4>
          <ul>
            <li>Research surveys (universities, research labs)</li>
            <li>Public‑service and municipal feedback (transport, clinics, city services)</li>
            <li>Clarity testing of official letters, health instructions and notices</li>
            <li>Cultural micro‑stories for museums, archives and libraries</li>
            <li>Short “community pulse” signals (accessibility issues, daily barriers)</li>
          </ul>

          <h4>Data handling</h4>
          <ul>
            <li>Responses → <strong>text only</strong></li>
            <li><strong>No audio storage</strong></li>
            <li><strong>No emotional/semantic analysis</strong></li>
            <li>Participation only with ongoing consent</li>
          </ul>
        </div>
      </section>

      {/* WHO CAN USE IT */}
      <section className="section-subtle">
        <div className="container-narrow">
          <h2>WHO CAN USE IT — AND HOW</h2>
          <h3>Verified Finnish institutions only</h3>

          <p>Access is restricted to organizations with official institutional domains.</p>

          <h4>Universities & Research Institutes</h4>
          <p>
            Upload surveys → receive anonymized responses for academic studies, social sciences,
            UX and public health research.
          </p>

          <h4>Municipalities & Public Agencies</h4>
          <p>
            Submit tasks like service-quality checks, clarity tests, city service evaluations,
            local accessibility signals. Older adults complete them by phone; text responses arrive within hours.
          </p>

          <h4>Cultural Institutions</h4>
          <p>
            Collect lived‑experience micro‑stories, local history fragments and reflections for exhibitions.
          </p>

          <h4>UX & Research Teams in Public Services</h4>
          <p>
            Test comprehension of instructions, reactions to service descriptions and accessibility of public information.
          </p>

          <h4>NOT permitted</h4>
          <ul>
            <li>Marketing</li>
            <li>Sales outreach</li>
            <li>Political content</li>
            <li>Commercial cold‑calling</li>
          </ul>
        </div>
      </section>

      {/* WHY IT MATTERS */}
      <section className="section-bordered">
        <div className="container-narrow">
          <h2>WHY THIS MATTERS FOR OLDER ADULTS</h2>
          <h3>Real participation. Zero digital friction.</h3>

          <ul>
            <li>Only a phone call — no apps, logins or interfaces</li>
            <li>Short, manageable tasks (30–90 seconds)</li>
            <li>No personal data collected</li>
            <li>No long interviews</li>
            <li>Adaptive timing based on comfort (paralinguistic cues only)</li>
          </ul>

          <p>
            They contribute to research, city services, healthcare clarity, cultural memory and
            accessibility improvements — <strong>with dignity, autonomy and on their own terms.</strong>
          </p>
        </div>
      </section>

      {/* SUMMARY */}
      <section className="spacious centered">
        <div className="container-narrow">
          <h2>ONE‑SENTENCE SUMMARY</h2>
          <p>
            A secure, AR4U‑integrated voice platform enabling verified Finnish institutions to gather anonymized
            contributions from older adults — powering research, public services and cultural memory without digital barriers.
          </p>
        </div>
      </section>
    </main>
  );
}
