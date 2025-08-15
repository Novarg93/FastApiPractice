import 'axios'

declare module 'axios' {
  export interface AxiosRequestConfig {
    /** Не делать редирект на /login в интерсепторе при 401 */
    __skipAuthRedirect?: boolean
  }
}