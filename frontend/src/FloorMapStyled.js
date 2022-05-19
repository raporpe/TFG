import styled from 'styled-components';






export const Flex = styled.div`
  display:flex;
`

export const C1 = styled.div`
  height: 610px;
  width: 190px;
  cursor: pointer;
  box-shadow: inset 0px 0px 0px 1px black;
  background-color: ${props => props.inputColor || "white"};
`

export const C2 = styled.div`
  height: 150px;
  width: 240px;
  text-align: center;
  cursor: pointer;
  padding: 30px 0px 0px 0px;
  background-color: ${props => props.inputColor || "white"};
  box-shadow: inset 0px 0px 0px 1px black;
`

export const C3 = styled.div`
  height: 150px;
  cursor: pointer;
  width: 200px;
  text-align: center;
  padding: 30px 0px 0px 0px;
  background-color: ${props => props.inputColor || "white"};
   box-shadow: inset 0px 0px 0px 1px black;
`

export const C4 = styled.div`
  height: 250px;
  width: 240px;
  text-align: center;
  background-color: ${props => props.inputColor || "white"};
  box-shadow: inset 0px 0px 0px 1px black;
`

export const C5 = styled.div`
  cursor: pointer;
  height: 180px;
  width: 200px;
  text-align: center;
  padding: 70px 0px 0px 0px;
  background-color: ${props => props.inputColor || "white"};
  box-shadow: inset 0px 0px 0px 1px black;
`

export const C6 = styled.div`
  height: 150px;
  cursor: pointer;
  width: 440px;
  text-align: center;
  background-color: ${props => props.inputColor || "white"};
  vertical-align: middle;
  box-shadow: inset 0px 0px 0px 1px black;
`


