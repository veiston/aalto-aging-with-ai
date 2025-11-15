import Button from "../_block/button/button";

import styles from "./hero.module.css";

import { useRouter } from "next/navigation";

const Hero = () => {

	const handleButtonClick = () => {
		
	};

	return (
		<section className={styles["hero"]}>
			<div className={`${styles["hero__container"]} layout`}>
				<div className={styles["hero__content"]}>
					<div className={styles["hero__header"]}>
						<h1 className={styles["hero__title"]}>
							<p className="text-display text-w-200">Easy Call Help</p>
							<p className="text-display text-w-200">
								A Voice Platform{" "}
								<span className="text-w-800">
									That Lets Older Adults Shape Society
								</span>
							</p>
							{/* <p className="text-display">
								<span className="text-w-800">Surveys. Public‑service feedback. Clarity checks. Cultural micro‑stories.</span>{" "}
								<span className="text-outlined text-w-800">
									All delivered via adaptive, safe phone interactions.<br />
								</span>
							</p> */}
							{/* <p className="text-display text-w-200">
								No digital barriers.{" "}
								<span className="text-w-800">No audio stored.</span>
							</p> */}
						</h1>
						<p className={styles["hero__subtitle"]}>
							A secure phone-based system where older adults contribute to research, public services and cultural projects as active participants whose voices matter.

							{/* We transform official surveys, service evaluations, clarity tests and cultural assignments
							into structured voice dialogues. Delivered entirely through <strong>AR4U</strong>, a trusted
							voice companion already used by older adults. */}
						</p>
					</div>
					<div className={styles["hero__bar"]}>
						<Button onClick={() => router.push("/dashboard")}>
							Go to Researcher Portal
						</Button>
						{/* <a href="https://github.com/x-bananer" target="_blank">
							<Button type="square" effect="light">
								<FaGithub size={24}></FaGithub>
							</Button>
						</a>
						<a href="https://www.linkedin.com/in/kseniia-shlenskaia-502004353/" target="_blank">
							<Button type="square" effect="light">
								<FaLinkedin size={24}></FaLinkedin>
							</Button>
						</a>
						<a href="mailto:kseniia.shlenskaia@gmail.com?subject=Portfolio Inquiry">
							<Button type="square" effect="light">
								<BiLogoGmail size={24}></BiLogoGmail>
							</Button>
						</a> */}
					</div>
				</div>
				{/* <div className={styles["hero__background"]}>
					<img
						className={styles["hero__image"]}
						src={hero}
						alt="Girl banner | Kseniia Shlenskaia | Frontend Dev"
					/>
				</div> */}
			</div>
		</section>
	);
};

export default Hero;
