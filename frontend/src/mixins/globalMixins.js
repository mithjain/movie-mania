import axios from 'axios';

let globalMixins = {
  methods: {
    getBaseURL: function () {
      /** Function to get the base url for API request */
      let baseUrl;
      if (process.env.NODE_ENV === 'development') {
        baseUrl = window.location.protocol + '//' +
          window.location.hostname + ':8000';
      } else {
        if (! window.location.origin) {
          window.location.origin = window.location.protocol + '//' + window.location.hostname + (
            window.location.port ? ':' + window.location.port : ''
          );
        }
        baseUrl = window.location.origin;
      }
      return baseUrl;
    },
    encodeURI: function (uri) {
      return encodeURIComponent(uri);
    },
    getQueryParams: function (params) {
      // build query params from a object
      if (! params) {
        return '';
      }
      let parameters = Object.keys(params);
      let queryParam = '?';
      parameters.forEach((parameter, index) => {
        if (index !== 0) {
          queryParam += '&';
        }
        queryParam += `${ parameter }=${ this.encodeURI(params[parameter]) }`;
      });
      return queryParam;
    },
    axiosPromise: function (
      {
        url, method = null, data = null, responseType = 'json', queryParams = null
      }
    ) {
      /**
       * Global function for making server request
       * @param: {
       *   url:               url to hit,
       *   method:            request type, 'GET', 'POST', 'PUT', 'PATCH', 'Delete', etc
       *   data:              data to send with request
       *   header:            custom headers for the request
       *   queryParams:       query params for url,
       *   responseType:      what format the response needs to be converted
       *   onUploadProgress:  if upload progress percent is needed
       *   notify:            flag for automated notifications on error
       *   setUser:           should the user data be updated after `this` API call
       * }
       **/

        // this order matters, put static first, then override everything requester sends
      const headers = {
          ...{
            'Content-Type': 'application/json; charset=utf-8;'
          }
        };
      let queryString = this.getQueryParams(queryParams);
      if (queryString.length > 0) {
        url += queryString;
      }
      return new Promise((resolve, reject) => {
        axios({
          url: url,
          baseURL: this.getBaseURL(),
          method: method,
          data: data,
          headers: headers,
          responseType: responseType
        }).then(response => {
          resolve(response.data);
        }).catch(error => {
          if (error.response) {
            const response = error.response;
            console.log(response.status);
          } else {
            // Something happened in setting up the request and triggered an Error
            console.log('unknown error', error);
          }
          reject(error);
        });
      });
    },
    getParentComponentByName: function (child, parentName) {
      let component = null;
      let parent = child.$parent;
      while (parent && ! component) {
        if (parent.$options.name === parentName) {
          component = parent;
        }
        parent = parent.$parent;
      }
      return component;
    },
    getAllChildrenByName: function (parent, childType) {
      let children = Array.from(parent.$children);
      let childInstances = [];
      children.forEach(child => {
          if (child.$options.name === childType) {
            childInstances.push(child);
          } else {
            childInstances = childInstances.concat(this.getAllChildrenByName(child, childType));
          }
        }
      );
      return childInstances;
    },
  }
};

export default globalMixins;