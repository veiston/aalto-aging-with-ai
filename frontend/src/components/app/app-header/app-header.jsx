import { useState, useEffect } from "react";

import Button from "../../../components/_block/button/button";

import styles from "./app-header.module.css";

import { useRouter } from "next/navigation";

const AppHeader = ({ children }) => {
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
				<span className="text-w-800 text-display">ECH</span>
				{children}
				<Button onClick={() => router.push("/dashboard/surveys")}>
					Sign In As a Researcher
				</Button>
			</div>
		</div>
	);
};

export default AppHeader;
