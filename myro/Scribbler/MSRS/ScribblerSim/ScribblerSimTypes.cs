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
using System.Runtime.Serialization;
using W3C.Soap;
using scribblersim = IPRE.ScribblerSim;


namespace IPRE.ScribblerSim
{
    
    /// <summary>
    /// ScribblerSim Contract
    /// </summary>
    public sealed class Contract
    {
        /// The Unique Contract Identifier for the ScribblerSim service
        public const String Identifier = "http://www.roboteducation.org/scribblersim.html";
    }

    public class ScribblerSimOperations : PortSet<DsspDefaultLookup, DsspDefaultDrop>
    {
    }

    [DataContract()]
    public class ScribblerSimState
    {
    }

}
