function RetrievedText(props) {
  const { text, rank } = props

  return (
    <div>
      {rank + ": " + text}
    </div>
  )
}

export default RetrievedText