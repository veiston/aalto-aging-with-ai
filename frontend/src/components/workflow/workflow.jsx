import styles from "./workflow.module.css";

import Media from "../_block/media/media";

const Workflow = () => {
  return (
    <div className={styles["workflow"]}>
      <div className={`${styles["workflow__container"]} layout`}>
        <div className={styles["workflow__header"]}>
          <h2 className={styles["workflow__title"]}>
            <span className="text-display">How ECH</span>{" "}
            <span className="text-display text-w-800">Works</span>
          </h2>
        </div>
        <div className={styles["workflow__content"]}>
          <ul className={styles["workflow__list"]}>
            <li>
              <Media
                number="1"
                title="A verified public institution submits a task"
                description="A municipality, research unit, health authority, cultural institution or library creates a survey, clarity test, or service-feedback flow request using the built-in editor of the ECH platform. The editor supports open questions, multiple choice, yes/no, scales and structured inputs."
                isReversed={false}
              />
            </li>
            <li>
              <Media
                number="2"
                title="The platform converts the task into a voice-ready script"
                description="Questions are transformed into natural, phone-optimized dialogue that older adults can easily follow."
                isReversed={true}
              />
            </li>
            <li>
              <Media
                number="3"
                title="The system delivers the task through a phone-based assistant"
                description="The assistant already operates nationwide and contacts only those older adults who previously gave informed, ongoing consent for participation."
                isReversed={false}
              />
            </li>
            <li>
              <Media
                number="4"
                title="Older adults respond by voice"
                description="The assistant reads all questions aloud and listens to spoken answers. Participants simply talk. No buttons and no digital interaction."
                isReversed={true}
              />
            </li>
            <li>
              <Media
                number={5}
                title="The institution receives the results in its dashboard in the text format"
                description="Responses become clean, structured text. Audio is not stored, no emotion or semantic profiling is performed. A safety filter removes personal data if it was mentioned accidentally."
                isReversed={false}
              />
            </li>
            <li>
              <Media
                number={6}
                title="Responses become clean, structured text"
                description="Audio is not stored, no emotion or semantic profiling is performed. A safety filter removes personal data if it was mentioned accidentally."
                isReversed={true}
              />
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Workflow;
