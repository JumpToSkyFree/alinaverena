import{r as s}from"./react-vRFa62LC.js";var N=function(){var r=function(i,n){return r=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var f in t)Object.prototype.hasOwnProperty.call(t,f)&&(e[f]=t[f])},r(i,n)};return function(i,n){if(typeof n!="function"&&n!==null)throw new TypeError("Class extends value "+String(n)+" is not a constructor or null");r(i,n);function e(){this.constructor=i}i.prototype=n===null?Object.create(n):(e.prototype=n.prototype,new e)}}(),k=function(){return k=Object.assign||function(r){for(var i,n=1,e=arguments.length;n<e;n++){i=arguments[n];for(var t in i)Object.prototype.hasOwnProperty.call(i,t)&&(r[t]=i[t])}return r},k.apply(this,arguments)},Q=function(r){return typeof window=="object"&&window.matchMedia?window.matchMedia(r).matches:!1};function R(r){var i={};return Object.keys(r).forEach(function(n){var e=r[n];i[n]=typeof e=="string"?Q(e):e}),i}var U=function(r){N(i,r);function i(n){var e=r.call(this,n)||this;if(e.state={matches:{},matchers:{},keys:[]},e.updateMatches=function(){return e.setState(function(u){var d=u.keys,j=u.matchers,M=u.matches;return{matches:d.reduce(function(p,y){return p[y]=j[y].matches,p},k({},M))}})},typeof window!="object"||!window.matchMedia)return e;var t=n.queries,f=Object.keys(t);return e.state.keys=f,Object.keys(t).forEach(function(u){var d=t[u];typeof d=="string"?e.state.matches[u]=(e.state.matchers[u]=window.matchMedia(d)).matches:e.state.matches[u]=d}),e}return i.prototype.componentDidMount=function(){var n=this,e=this.state.matchers;Object.keys(e).forEach(function(t){return e[t].addEventListener("change",n.updateMatches)})},i.prototype.componentWillUnmount=function(){var n=this,e=this.state.matchers;Object.keys(e).forEach(function(t){return e[t].removeEventListener("change",n.updateMatches)})},i.prototype.render=function(){var n=this.props.children,e=this.state.matches;return n(e)},i}(s.Component);function $(r,i){for(var n=Object.keys(r),e=n.length,t=0;t<e&&!i[n[t]];t++);return n[t]}function C(r,i,n,e){for(var t=Object.keys(r),f=t.length,u=0;u<f&&!i[t[u]];u++);for(;u>=0;u--){var d=n[t[u]];if(d!==void 0)return d}return e}function _(r,i){var n=Object.keys(r);return n.reduce(function(e,t){return i[t]!==void 0&&(e[t]=i[t]),e},{})}function S(r,i,n,e,t){var f=!1;return Object.keys(r).reduce(function(u,d){return e&&i[d]&&(f=!0),u[d]=(t?f:!f)?null:n,!e&&i[d]&&(f=!0),u},{})}function W(r){return Object.keys(r).reduce(function(i,n){return i[n]=!1,i},{})}function A(r){return Object.keys(r).reduce(function(i,n){return r[n]!==void 0&&(i[n]=r[n]),i},{})}var h=function(){return h=Object.assign||function(r){for(var i,n=1,e=arguments.length;n<e;n++){i=arguments[n];for(var t in i)Object.prototype.hasOwnProperty.call(i,t)&&(r[t]=i[t])}return r},h.apply(this,arguments)},w=function(r,i){var n={};for(var e in r)Object.prototype.hasOwnProperty.call(r,e)&&i.indexOf(e)<0&&(n[e]=r[e]);if(r!=null&&typeof Object.getOwnPropertySymbols=="function")for(var t=0,e=Object.getOwnPropertySymbols(r);t<e.length;t++)i.indexOf(e[t])<0&&Object.prototype.propertyIsEnumerable.call(r,e[t])&&(n[e[t]]=r[e[t]]);return n},x={};function z(r,i){var n=R(r),e={},t=s.createContext(e),f=function(a){return a===e?n:a},u=function(a){return s.createElement(t.Consumer,null,function(o){return a(f(o))})};function d(a,o,c){return C(r,a,o,c)}function j(a,o){var c=f(s.useContext(t));return d(c,a,o)}function M(a,o){return C(r,a,o)}var p=function(a){var o=a.children,c=a.state,l=c===void 0?null:c;return s.createElement(t.Consumer,null,function(v){return s.createElement(U,{queries:r},function(O){var m=l||h(h({},v||{}),A(O));return s.createElement(t.Provider,{value:m,children:o})})})};p.propTypes=x;var y=function(a){var o=a.children;return u(function(c){return o(c,function(l){return d(c,l)})})};y.propTypes=x;var B=function(a){return u(function(o){return M(o,a)})},g=function(a){return u(function(o){return M(o,a)})};g.propTypes=x;var T=function(a){var o=a.children,c=w(a,["children"]);return s.createElement(t.Provider,{value:_(r,h(h({},W(r)),c))},o)},D=function(a){var o=a.children,c=w(a,["children"]);return s.createElement(t.Consumer,null,function(l){var v=h(h({},A(l)),_(r,c));return s.createElement(t.Provider,{value:v,children:o})})},I=function(a){var o=a.children,c=a.including,l=w(a,["children","including"]);return s.createElement(g,h({},S(r,l,o,!c,!0)))},H=function(a){var o=a.children,c=a.including,l=w(a,["children","including"]);return s.createElement(g,h({},S(r,l,o,!!c,!1)))},L=function(a){var o=a.predicted,c=a.hydrated,l=a.onWrongPrediction,v=a.children,O=s.useState(c===void 0?!1:c),m=O[0],G=O[1],b=s.useContext(t);s.useEffect(function(){G(c===void 0?!0:c)},[c]),s.useEffect(function(){m&&!b[o]&&l&&l(o,$(r,b))},[m]);var K=s.useMemo(function(){var E;return m?b:h(h({},W(r)),(E={},E[o]=!0,E))},[b,m]);return s.createElement(t.Provider,{value:K,children:v})},V=function(a){var o=a.predicted,c=a.hydrated,l=a.onWrongPrediction,v=a.children;return s.createElement(p,null,s.createElement(L,{predicted:o,hydrated:c,onWrongPrediction:l,children:v}))};return{queries:r,pickMatch:d,useMedia:j,Provider:p,Mock:T,Override:D,Matches:y,Inline:B,Above:H,Below:I,Matcher:g,ServerRender:V,Gearbox:t.Consumer,Consumer:t.Consumer}}const F={mobile:"(max-width: 767px)",tablet:"(max-width: 1023px)",desktop:"(min-width: 1024px)"};var P=z(F),X=P.Provider,Y=P.Below,Z=P.Above;export{Z as A,Y as B,X as P};
