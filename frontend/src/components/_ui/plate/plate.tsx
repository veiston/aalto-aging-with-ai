import styles from "./plate.module.scss";

import type { ReactNode } from "react";

interface UiPlateProps {
	title?: string;
	icon?: ReactNode;
}

const UiPlate = ({ title, icon }: UiPlateProps) => {
	return (
		<div className={styles["ui-plate"]}>
			{icon && (
				<div className={styles["ui-plate__icon"]}>
					{icon}
				</div>
			)}
			{title && (
				<p className={styles["ui-plate__title"]}>
					{title}
				</p>
			)}
		</div>
	);
};

export default UiPlate;