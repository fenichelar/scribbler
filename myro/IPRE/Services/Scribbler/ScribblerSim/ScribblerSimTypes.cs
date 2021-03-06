// Copyright (c) Microsoft Corporation.  All rights reserved.

//------------------------------------------------------------------------------
// ScribblerSimTypes.cs
//
//     This code was generated by the DssNewService tool.
//
//------------------------------------------------------------------------------
using Microsoft.Ccr.Core;
using Microsoft.Dss.ServiceModel.Dssp;
using System;
using System.Collections.Generic;
using Microsoft.Dss.Core.Attributes;
using W3C.Soap;
using Microsoft.Dss.Core.DsspHttp;


namespace Myro.Services.ScribblerSim
{
    [DataContract()]
    public class ScribblerSimState
    {
        [DataMember]
        public int Cubes;
    }

    /// <summary>
    /// ScribblerSim Contract
    /// </summary>
    public static class Contract
    {
        public const string Identifier = "http://www.roboteducation.org/schemas/2008/06/scribblersim.html";
    }

    public class ScribblerSimOperations : PortSet<
        DsspDefaultLookup, 
        DsspDefaultDrop,
        Get,
        Replace>
    {
    }

    public class Get : Get<GetRequestType, PortSet<ScribblerSimState, Fault>>
    {
    }

    public class Replace : Replace<ScribblerSimState, DsspResponsePort<DefaultReplaceResponseType>>
    {
    }

}
