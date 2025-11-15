import Button from "../_block/button/button";

import styles from "./hero.module.css";

import { useRouter } from "next/navigation";

const Hero = () => {

	const handleButtonClick = () => {
		
	};

	const router = useRouter();

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
						</h1>
						<p className={styles["hero__subtitle"]}>
							A secure phone-based system where older adults contribute to research, public services and cultural projects as active participants whose voices matter.
						</p>
					</div>
					<div className={styles["hero__bar"]}>
						<Button onClick={() => router.push("/dashboard/surveys")}>
							Go to Researcher Portal
						</Button>
					</div>
				</div>
			</div>
		</section>
	);
};

export default Hero;
