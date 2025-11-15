import styles from "./about.module.css";

import about from "../../assets/images/about.png";

const About = () => {
	const DESCRIPTION = `Across Finland, many institutions depend on public input: municipalities need service feedback, THL and HUS test how clear health instructions are, Kela evaluates communication effectiveness, VR and Traficom review user experience, and museums and libraries collect lived-experience stories.
						\nAll these tasks require answers from real people, yet most groups are either overloaded or difficult to reach. Older adults, however, consistently show a high willingness to respond by phone and can provide detailed, experience-based input that institutions currently lack.
						\nThis platform uses that capacity: older adults contribute through simple phone calls, and institutions receive stable, high-quality responses without digital barriers.
						\nThe participation and involvement keeps older adults mentally engaged, socially connected, and directly involved in decisions that affect their daily lives — all through simple phone conversations, without requiring digital skills or new devices.`;

	return (
		<div className={styles["about"]}>
			<div className={`${styles["about__container"]} layout`}>
				<div className={styles["about__background"]}>
					<img
						className={styles["about__image"]}
						src={about.src}
						alt="Icon. Laptop. Mobile phone"
					/>
				</div>
				<div className={styles["about__content"]}>
					<h2 className={styles["about__title"]}>
						<span className="text-display">About </span>{" "}
						<span className="text-display text-w-800">ECH</span>
					</h2>
					<div className={styles["about__description"]}>
						{DESCRIPTION.split("\n").map((line, idx) => (
							<p key={idx} className="mb-s">
								{line}
							</p>
						))}
					</div>
				</div>
			</div>
		</div>
	);
};

export default About;
