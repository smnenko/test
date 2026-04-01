import React, { ChangeEventHandler } from "react";

type InputTextProps = Partial<HTMLInputElement> & {
  onChange: ChangeEventHandler<HTMLInputElement>;
  label?: string;
};

export const InputText: React.FC<InputTextProps> = ({
  onChange,
  label,
  ...props
}) => (
  <>
    <label
      style={{
        fontSize: 14,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {label}
      <input
        type={props.type}
        placeholder={props.placeholder}
        value={props.value}
        onChange={onChange}
        style={{
          padding: "8px 12px",
          border: "1px solid #ddd",
          borderRadius: 4,
          fontSize: 14,
          width: "100%",
          maxWidth: "20rem",
          appearance: "textfield"
        }}
        {...props}
      />
    </label>
  </>
);
