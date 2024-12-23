import React, { useState } from "react";
import { Link } from "react-router-dom";

const FAQ = () => {
  const [showAnswer, setShowAnswer] = useState([
    false,
    false,
    false,
    false,
    false,
  ]);

  const changeShowAnswer = (index: number) => {
    setShowAnswer((prev) => {
      prev[index] = !prev[index];
      return [...prev];
    });
  };

  return (
    <div className="bg-cool-gray w-full min-h-screen py-28 px-16 flex items-center justify-center text-white">
      <div className="flex flex-col h-full w-full gap-20 items-center justify-center">
        <div className="flex flex-col flex-wrap w-full h-fit gap-7 items-center px-40">
          <h1 className="text-6xl">FAQs</h1>
          <p>Find answers to common questions regarding your login</p>
        </div>
        <div className="flex flex-col w-full px-40">
          <div className="flex flex-col border-t border-b items-start justify-center p-4">
            <div className="flex justify-between w-full align-center">
              <h1 className="text-lg leading-7">How do I reset?</h1>
              <a
                className="text-lg leading-7 rounded-lg p-2"
                onClick={() => changeShowAnswer(0)}
              >
                {showAnswer[0] ? (
                  <img src={require("../assets/img/Vector-right.png")} alt="" />
                ) : (
                  <img src={require("../assets/img/Vector.png")} alt="" />
                )}
              </a>
            </div>
            {showAnswer[0] && (
              <p className="my-4">
                To reset your password, click on the 'Forgot Password?' link on
                the login page. Follow the prompts to receive a password reset
                email. Check your inbox and follow the instructions provided.
              </p>
            )}
          </div>
          <div className="flex flex-col border-t border-b items-start justify-center p-4">
            <div className="flex justify-between w-full align-center">
              <h1 className="text-lg leading-7">How do I change my email?</h1>
              <a
                className="text-lg leading-7 rounded-lg p-2"
                onClick={() => changeShowAnswer(1)}
              >
                {showAnswer[1] ? (
                  <img src={require("../assets/img/Vector-right.png")} alt="" />
                ) : (
                  <img src={require("../assets/img/Vector.png")} alt="" />
                )}
              </a>
            </div>
            {showAnswer[1] && (
              <p className="my-4">
                To change your email, go to the account settings page and update
                your email address. Confirm the change through the verification
                email sent to your new address.
              </p>
            )}
          </div>
          <div className="flex flex-col border-t border-b items-start justify-center p-4">
            <div className="flex justify-between w-full align-center">
              <h1 className="text-lg leading-7">How do I delete my account?</h1>
              <a
                className="text-lg leading-7 rounded-lg p-2"
                onClick={() => changeShowAnswer(2)}
              >
                {showAnswer[2] ? (
                  <img src={require("../assets/img/Vector-right.png")} alt="" />
                ) : (
                  <img src={require("../assets/img/Vector.png")} alt="" />
                )}
              </a>
            </div>
            {showAnswer[2] && (
              <p className="my-4">
                To delete your account, go to the account settings page and
                select the 'Delete Account' option. Follow the prompts to
                confirm the deletion.
              </p>
            )}
          </div>
          <div className="flex flex-col border-t border-b items-start justify-center p-4">
            <div className="flex justify-between w-full align-center">
              <h1 className="text-lg leading-7">How do I contact support?</h1>
              <a
                className="text-lg leading-7 rounded-lg p-2"
                onClick={() => changeShowAnswer(3)}
              >
                {showAnswer[3] ? (
                  <img src={require("../assets/img/Vector-right.png")} alt="" />
                ) : (
                  <img src={require("../assets/img/Vector.png")} alt="" />
                )}
              </a>
            </div>
            {showAnswer[3] && (
              <p className="my-4">
                To contact support, visit the support page and fill out the
                contact form. Our support team will get back to you as soon as
                possible.
              </p>
            )}
          </div>
          <div className="flex flex-col border-t border-b items-start justify-center p-4">
            <div className="flex justify-between w-full align-center">
              <h1 className="text-lg leading-7">How do I update my profile?</h1>
              <a
                className="text-lg leading-7 rounded-lg p-2"
                onClick={() => changeShowAnswer(4)}
              >
                {showAnswer[4] ? (
                  <img src={require("../assets/img/Vector-right.png")} alt="" />
                ) : (
                  <img src={require("../assets/img/Vector.png")} alt="" />
                )}
              </a>
            </div>
            {showAnswer[4] && (
              <p className="my-4">
                To update your profile, go to the profile settings page and make
                the necessary changes. Save your updates to apply the changes to
                your profile.
              </p>
            )}
          </div>
        </div>
        <div className="flex flex-col w-full gap-7 items-center px-40">
          <h1 className="text-3xl">Still have Questions?</h1>
          <p className="text-xl leading-7">
            Reach out to our support team for assitance.
          </p>
          <Link
            className="border-2 border-white rounded-lg py-4 px-6"
            to="/contact"
          >
            Contact
          </Link>
        </div>
      </div>
    </div>
  );
};

export default FAQ;
