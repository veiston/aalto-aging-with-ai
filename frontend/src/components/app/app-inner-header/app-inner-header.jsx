import { useState, useEffect } from "react";

import Button from "../../_block/button/button";

import styles from "./app-inner-header.module.css";

import { useRouter } from "next/navigation";

const AppInnerHeader = ({ children }) => {
	const [hasShadow, setHasShadow] = useState(false);

	const router = useRouter();

	useEffect(() => {
		const handleScroll = () => {
			setHasShadow(window.scrollY > 0);
		};

		window.addEventListener("scroll", handleScroll);
		return () => window.removeEventListener("scroll", handleScroll);
	}, []);

	return (
		<div
			className={`${styles["app-header"]} ${hasShadow && styles["app-header--shadowed"]
				}`}
		>
			<div className={`${styles["app-header__container"]} layout`}>
				<div>
					<div className="text-w-800 text-display">ECH


					</div>
					<div className="text-w-400 text-p3">Researcher’s dashboard</div>
				</div>

				<Button type="link" onClick={() => router.push("/dashboard/surveys")}>
					My surveys
				</Button>
				<Button type="link" onClick={() => router.push("/dashboard/surveys/create")}>
					Add a survey
				</Button>
				<Button type="link">
					Settings
				</Button>
				<Button effect="light" onClick={() => router.push("/")}>
					Sign Out
				</Button>
			</div>
		</div>
	);
};

export default AppInnerHeader;
