function Footer(props) {

  return (
    <div>

      <div>
        <p>{"Click "}
          <a href="https://github.com/sertman1/www.lovelylatin.com">here</a> for source code.
        </p>
        <p>{"A special thank you to Colonel William Whitaker and his "}
          <a href="https://latin-words.com/">Words</a>.
        </p>
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <p>Made with 🌈 🍀 ✨ in Charm City</p>

      </div>

    </div>
  )
}

export default Footer;