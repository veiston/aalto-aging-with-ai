import styles from "./contact.module.css";

import Button from "../_block/button/button";

import { useRouter } from "next/navigation";

const Contact = () => {
  const router = useRouter();

  return (
    <div className={styles["contact"]}>
      <div className={`${styles["contact__container"]} layout`}>
        <p className="text-display text-w-200">
          This is where research <br></br> meets participation{" "}
          <br></br>
          <span className="text-w-800">
            This is where participation <br></br> provides impact
          </span>
        </p>
        <div className={styles["contact__button"]}>
          <Button onClick={() => router.push("/dashboard/surveys")}>
            Sign Up As A Resercher
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Contact;
