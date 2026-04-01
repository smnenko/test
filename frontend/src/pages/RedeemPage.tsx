import axios from "axios";
import { InputText } from "../components/InputText";
import { API_URL } from "../constants/api";
import { ChangeEvent, useState } from "react";

const RedeemPage = () => {
  const [code, setCode] = useState("");
  const [amount, setAmount] = useState<number>();
  const [errors, setErrors] = useState("");
  const [balance, setBalance] = useState("");

  const handleSubmit = (e: ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (code && amount) {
      const url = `${API_URL}/api/gift-cards/${code}/redeem`;

      axios
        .post(url, { amount })
        .then((response) => {
          setBalance(response.data.balance);
        })
        .catch((error) => {
          setErrors(error.response.data.detail);
          setBalance("");
        });
    }
  };

  const handleCodeChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.value) setErrors("Введите код")
    else {
      setCode(e.target.value);
      setErrors('')
    }
  };

  const handleAmountChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (!e.target.value || Number(e.target.value) <= 0) setErrors("Cумма списания должна быть больше 0")
    else {
      setAmount(Number(e.target.value))
      setErrors('')
    }
  };

  return (
    <>
      <h1 style={{ marginBottom: 20 }}>Списание с гифт-карты</h1>
      <div style={{ display: "flex", gap: 16, flexDirection: "column" }}>
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 24,
            backgroundColor: "white",
            maxWidth: 400,
          }}
        >
          <form
            onSubmit={handleSubmit}
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 16,
            }}
          >
            <InputText
              label="Код гифт-карты"
              placeholder="Введите код..."
              onChange={handleCodeChange}
              minLength="0"
            />
            <InputText
              type="number"
              inputmode="decimal"
              label="Сумма списания"
              placeholder="Введите сумму..."
              onChange={handleAmountChange}
              min="0"
              step="0.01"
            />

            {errors ? (
              <p style={{ color: "var(--color-error)" }}>{errors}</p>
            ) : undefined}
            <button
              style={{
                fontSize: "16px",
                background:
                  !amount || !code || errors
                    ? "var(--color-bg)"
                    : "var(--color-primary)",
                color: amount && code && !errors ? "white" : "",
                padding: " 0.7em 1em",
                paddingLeft: " 0.9em",
                borderRadius: "16px",
                border: "none",
                cursor: "pointer",
                maxWidth: "20rem",
              }}
              disabled={!amount || !code || !!errors}
            >
              Списать
            </button>
          </form>
        </div>
        {balance ? (
          <div
            style={{
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: 24,
              backgroundColor: "white",
              maxWidth: 400,
            }}
          >
            <p>Остаток на гифт-карте: {balance}</p>
          </div>
        ) : undefined}
      </div>
    </>
  );
};

export default RedeemPage;
